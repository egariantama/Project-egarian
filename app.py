import datetime
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# --- 🎯 Simulasi Data Pipeline ---
# Struktur data yang mewakili status pipeline di berbagai cabang
PIPELINE_STATUS = {
    "JKT-001": {
        "status": "SUCCESS",
        "last_run": datetime.datetime(2025, 12, 8, 22, 0, 0),
        "metrics": {"records_processed": 15000, "duration_sec": 120},
        "description": "Pipeline Pengambilan Data Harian Kas"
    },
    "BDG-002": {
        "status": "RUNNING",
        "last_run": datetime.datetime(2025, 12, 8, 23, 5, 0),
        "metrics": {"records_processed": 8000, "duration_sec": 65},
        "description": "Pipeline Sinkronisasi Data CRM"
    },
    "SBY-003": {
        "status": "FAILED",
        "last_run": datetime.datetime(2025, 12, 8, 18, 30, 0),
        "metrics": {"records_processed": 0, "duration_sec": 10},
        "description": "Pipeline Laporan Keuangan Mingguan"
    },
    "SMG-004": {
        "status": "SUCCESS",
        "last_run": datetime.datetime(2025, 12, 8, 21, 15, 0),
        "metrics": {"records_processed": 5000, "duration_sec": 45},
        "description": "Pipeline Log Transaksi Real-time"
    },
}

# --- ⚙️ Fungsi Monitoring Utama ---

def get_overall_summary():
    """Menghitung ringkasan status keseluruhan."""
    summary = {
        "total_pipelines": len(PIPELINE_STATUS),
        "success": sum(1 for data in PIPELINE_STATUS.values() if data['status'] == 'SUCCESS'),
        "running": sum(1 for data in PIPELINE_STATUS.values() if data['status'] == 'RUNNING'),
        "failed": sum(1 for data in PIPELINE_STATUS.values() if data['status'] == 'FAILED'),
    }
    return summary

def get_detailed_status():
    """Mengembalikan status detail per cabang, diurutkan berdasarkan waktu lari terakhir."""
    detailed_list = []
    for branch_id, data in PIPELINE_STATUS.items():
        # Memformat waktu agar lebih mudah dibaca di web
        formatted_time = data['last_run'].strftime("%Y-%m-%d %H:%M:%S")
        
        detail = {
            "branch_id": branch_id,
            "status": data['status'],
            "last_run": formatted_time,
            "description": data['description'],
            "records": data['metrics']['records_processed'],
            "duration": data['metrics']['duration_sec'],
        }
        detailed_list.append(detail)
        
    # Mengurutkan berdasarkan waktu lari terakhir
    detailed_list.sort(key=lambda x: datetime.datetime.strptime(x['last_run'], "%Y-%m-%d %H:%M:%S"), reverse=True)
    
    return detailed_list


# --- 🌐 Rute Flask (API & Web) ---

@app.route('/')
def dashboard():
    """Rute utama untuk menampilkan dashboard web."""
    summary = get_overall_summary()
    details = get_detailed_status()
    
    # Render template HTML
    return render_template('dashboard.html', summary=summary, details=details)

@app.route('/api/status')
def api_status():
    """Rute API untuk mendapatkan data dalam format JSON."""
    return jsonify({
        "summary": get_overall_summary(),
        "details": get_detailed_status()
    })

if __name__ == '__main__':
    # Untuk menjalankan aplikasi secara lokal
    # app.run(debug=True) 
    pass # Hanya kerangka, tidak dijalankan di lingkungan ini

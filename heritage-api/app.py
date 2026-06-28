from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)

SITES = {
    "lahore-fort": {
        "id": "lahore-fort",
        "name": "Lahore Fort",
        "city": "Lahore",
        "province": "Punjab",
        "era": "Mughal (1566 AD)",
        "status": "reconstructed",
        "photos": 340,
        "point_cloud_size": 2847291,
        "mesh_polygons": 892450,
        "method": "COLMAP + 3DGS",
        "scan_date": "2026-03-14",
        "reconstruction_hours": 4.2,
        "coverage_pct": 94.7,
        "lat": 31.5881,
        "lng": 74.3157,
        "description": "UNESCO World Heritage Site. Built by Emperor Akbar in 1566 AD, expanded under Jahangir and Shah Jahan. 13 gates, 21 notable monuments across 20 hectares.",
        "risk_level": "medium",
        "preservation_score": 72
    },
    "rohtas-fort": {
        "id": "rohtas-fort",
        "name": "Rohtas Fort",
        "city": "Jhelum",
        "province": "Punjab",
        "era": "Sur Empire (1541 AD)",
        "status": "in_progress",
        "photos": 180,
        "point_cloud_size": 1240000,
        "mesh_polygons": 440200,
        "method": "COLMAP + NeRF",
        "scan_date": "2026-04-02",
        "reconstruction_hours": 6.1,
        "coverage_pct": 71.3,
        "lat": 32.9418,
        "lng": 73.5844,
        "description": "Built by Sher Shah Suri in 1541 to resist Mughal expansion. Stretches 4 km in perimeter with 68 semi-circular bastions. UNESCO World Heritage Site.",
        "risk_level": "low",
        "preservation_score": 81
    },
    "mohenjo-daro": {
        "id": "mohenjo-daro",
        "name": "Mohenjo-daro",
        "city": "Larkana",
        "province": "Sindh",
        "era": "Indus Valley (2500 BC)",
        "status": "queued",
        "photos": 95,
        "point_cloud_size": 0,
        "mesh_polygons": 0,
        "method": "pending",
        "scan_date": None,
        "reconstruction_hours": 0,
        "coverage_pct": 0,
        "lat": 27.3242,
        "lng": 68.1376,
        "description": "One of the earliest major cities of the ancient Indus Valley civilization (2500 BCE). Faces critical deterioration. Priority target for digital preservation.",
        "risk_level": "critical",
        "preservation_score": 45
    },
    "badshahi-mosque": {
        "id": "badshahi-mosque",
        "name": "Badshahi Mosque",
        "city": "Lahore",
        "province": "Punjab",
        "era": "Mughal (1673 AD)",
        "status": "reconstructed",
        "photos": 220,
        "point_cloud_size": 1956000,
        "mesh_polygons": 612800,
        "method": "3DGS",
        "scan_date": "2026-02-20",
        "reconstruction_hours": 2.8,
        "coverage_pct": 97.2,
        "lat": 31.5882,
        "lng": 74.3098,
        "description": "Commissioned by Emperor Aurangzeb, completed 1673. One of the largest mosques globally. Iconic red sandstone facade with white marble domes.",
        "risk_level": "low",
        "preservation_score": 88
    }
}

METHODS = [
    {
        "id": "colmap",
        "name": "COLMAP",
        "subtitle": "Structure from Motion + MVS",
        "inputs": "50+ overlapping photos",
        "output": "Dense point cloud (.ply)",
        "gpu": False,
        "time": "2-8 hrs",
        "quality": 4,
        "realtime": False,
        "pmw_use": "Foundation for all pipelines"
    },
    {
        "id": "nerf",
        "name": "NeRF",
        "subtitle": "Neural Radiance Fields",
        "inputs": "20-200 calibrated images",
        "output": "Implicit neural scene",
        "gpu": True,
        "time": "4-12 hrs",
        "quality": 5,
        "realtime": False,
        "pmw_use": "Photorealistic archival renders"
    },
    {
        "id": "3dgs",
        "name": "3D Gaussian Splatting",
        "subtitle": "Real-time Gaussian Splats",
        "inputs": "Calibrated images + COLMAP poses",
        "output": "Gaussian splat scene (.splat)",
        "gpu": True,
        "time": "20-45 min",
        "quality": 5,
        "realtime": True,
        "pmw_use": "Explorable worlds (PMW primary target)"
    },
    {
        "id": "midas",
        "name": "MiDaS",
        "subtitle": "Monocular Depth Estimation",
        "inputs": "Single image or video",
        "output": "Relative depth map",
        "gpu": False,
        "time": "Instant",
        "quality": 2,
        "realtime": True,
        "pmw_use": "Quick scan from single photo"
    }
]

PIPELINE_STAGES = {
    "colmap": ["feature_extraction", "feature_matching", "sfm_triangulation", "dense_mvs", "surface_meshing"],
    "nerf": ["colmap_pose_estimation", "ray_sampling", "nerf_training", "novel_view_synthesis"],
    "3dgs": ["colmap_pose_estimation", "gaussian_initialization", "splat_optimization", "realtime_export"],
    "midas": ["depth_inference", "back_projection", "pointcloud_export"]
}

EST_HOURS = {"colmap": 4.5, "nerf": 8.0, "3dgs": 0.55, "midas": 0.05}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/react")
def react_app():
    return send_from_directory(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "react-app"),
        "index.html"
    )


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "EchoFrame Heritage Reconstruction API",
        "version": "1.0.0",
        "team": "EchoFrame Labs",
        "track": "AI-Based 3D Scene Reconstruction",
        "internship": "PreserveMy.World x TechRealm 2026",
        "sites_loaded": len(SITES),
        "methods_available": len(METHODS)
    })


@app.route("/api/sites")
def list_sites():
    summary_keys = ("id", "name", "city", "era", "status", "photos", "method", "preservation_score", "risk_level", "coverage_pct")
    return jsonify({
        "count": len(SITES),
        "sites": [{k: v for k, v in s.items() if k in summary_keys} for s in SITES.values()]
    })


@app.route("/api/sites/<site_id>")
def get_site(site_id):
    site = SITES.get(site_id)
    if not site:
        return jsonify({
            "error": f"Site '{site_id}' not found",
            "available_ids": list(SITES.keys())
        }), 404
    return jsonify(site)


@app.route("/api/sites/<site_id>/pointcloud")
def get_pointcloud(site_id):
    site = SITES.get(site_id)
    if not site:
        return jsonify({"error": "Site not found"}), 404

    if site["status"] == "queued":
        return jsonify({
            "error": "Reconstruction not started yet",
            "site": site["name"],
            "status": "queued",
            "hint": "Submit a POST to /api/reconstruct to queue this site"
        }), 202

    random.seed(hash(site_id) % (2 ** 31))
    sample = min(300, max(60, site["point_cloud_size"] // 5000))
    pts = []

    for _ in range(sample):
        r = random.random()
        if r < 0.32:
            pts.append({"x": round(random.uniform(-3, 3), 3), "y": round(random.uniform(0, 4), 3), "z": round(random.uniform(-0.12, 0.12), 3), "layer": "front_wall"})
        elif r < 0.52:
            pts.append({"x": round(random.uniform(-4, 4), 3), "y": round(random.uniform(-0.08, 0.08), 3), "z": round(random.uniform(0, 4), 3), "layer": "ground"})
        elif r < 0.67:
            pts.append({"x": round(random.uniform(-3, 3), 3), "y": round(random.uniform(3.9, 4.5), 3), "z": round(random.uniform(0, 4), 3), "layer": "roof"})
        elif r < 0.82:
            pts.append({"x": round(random.uniform(-3, 3), 3), "y": round(random.uniform(0, 4), 3), "z": round(3.9 + random.uniform(-0.12, 0.12), 3), "layer": "back_wall"})
        else:
            side = -3 if random.random() < 0.5 else 3
            pts.append({"x": round(side + random.uniform(-0.12, 0.12), 3), "y": round(random.uniform(0, 4), 3), "z": round(random.uniform(0, 4), 3), "layer": "side_wall"})

    return jsonify({
        "site": site["name"],
        "full_point_count": site["point_cloud_size"],
        "sample_returned": len(pts),
        "method": site["method"],
        "scan_date": site["scan_date"],
        "points": pts
    })


@app.route("/api/reconstruct", methods=["POST"])
def reconstruct():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({
            "error": "JSON body required",
            "example": {"site_id": "lahore-fort", "method": "colmap", "num_photos": 120}
        }), 400

    site_id = body.get("site_id")
    method = str(body.get("method", "colmap")).lower()
    num_photos = int(body.get("num_photos", 50))

    if not site_id:
        return jsonify({"error": "site_id is required"}), 400
    if site_id not in SITES:
        return jsonify({"error": f"Unknown site: {site_id}", "available": list(SITES.keys())}), 404
    if num_photos < 10:
        return jsonify({"error": "Minimum 10 photos required for reconstruction"}), 422
    if method not in PIPELINE_STAGES:
        return jsonify({"error": f"Unknown method: {method}", "valid": list(PIPELINE_STAGES.keys())}), 400

    est_h = round(EST_HOURS[method] * (num_photos / 100), 2)
    est_pts = int(num_photos * random.randint(7600, 9400))
    job_id = f"{site_id[:4].upper()}-{method[:3].upper()}-{random.randint(1000, 9999)}"

    return jsonify({
        "job_id": job_id,
        "status": "queued",
        "site": SITES[site_id]["name"],
        "method": method.upper(),
        "num_photos": num_photos,
        "pipeline_stages": PIPELINE_STAGES[method],
        "estimated_hours": est_h,
        "estimated_points": est_pts,
        "output_format": ".ply + .splat",
        "mission": "Preserving Pakistani heritage for future generations"
    }), 202


@app.route("/api/methods")
def list_methods():
    return jsonify({"count": len(METHODS), "methods": METHODS})


@app.route("/api/stats")
def get_stats():
    by_status = {}
    for s in SITES.values():
        by_status[s["status"]] = by_status.get(s["status"], 0) + 1

    total_photos = sum(s["photos"] for s in SITES.values())
    total_points = sum(s["point_cloud_size"] for s in SITES.values())
    critical = [s["name"] for s in SITES.values() if s["risk_level"] == "critical"]
    avg_score = round(sum(s["preservation_score"] for s in SITES.values()) / len(SITES), 1)

    return jsonify({
        "total_sites": len(SITES),
        "by_status": by_status,
        "total_photos_processed": total_photos,
        "total_3d_points": total_points,
        "critical_risk_sites": critical,
        "avg_preservation_score": avg_score
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

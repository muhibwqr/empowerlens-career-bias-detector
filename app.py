import os
import json
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CommunityAI - Find Local Resources</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container { max-width: 800px; margin: 0 auto; }

        header {
            text-align: center;
            padding: 40px 0 30px;
            color: white;
        }

        header h1 {
            font-size: 2.8rem;
            font-weight: 800;
            letter-spacing: -1px;
            margin-bottom: 8px;
        }

        header h1 span { color: #ffd700; }

        header p {
            font-size: 1.1rem;
            opacity: 0.9;
            margin-bottom: 6px;
        }

        .badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.4);
            color: white;
            padding: 3px 12px;
            border-radius: 20px;
            font-size: 0.78rem;
            margin-top: 6px;
        }

        .search-card {
            background: white;
            border-radius: 20px;
            padding: 32px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            margin-bottom: 24px;
        }

        .search-card h2 {
            font-size: 1.1rem;
            color: #4a5568;
            margin-bottom: 20px;
            font-weight: 600;
        }

        .form-row { display: flex; gap: 12px; flex-wrap: wrap; }

        .form-group { flex: 1; min-width: 200px; }

        .form-group label {
            display: block;
            font-size: 0.82rem;
            font-weight: 600;
            color: #718096;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .form-group input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            font-size: 1rem;
            transition: border-color 0.2s;
            outline: none;
            color: #2d3748;
        }

        .form-group input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.15);
        }

        .btn-search {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 32px;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            width: 100%;
            margin-top: 16px;
            transition: transform 0.15s, box-shadow 0.15s;
            letter-spacing: 0.3px;
        }

        .btn-search:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102,126,234,0.5);
        }

        .btn-search:active { transform: translateY(0); }

        .btn-search:disabled {
            opacity: 0.7;
            cursor: not-allowed;
            transform: none;
        }

        .examples {
            margin-top: 14px;
            font-size: 0.82rem;
            color: #a0aec0;
        }

        .examples span { font-weight: 600; color: #718096; }

        .example-chip {
            display: inline-block;
            background: #f7f8fa;
            border: 1px solid #e2e8f0;
            color: #667eea;
            padding: 3px 10px;
            border-radius: 12px;
            margin: 2px;
            cursor: pointer;
            font-size: 0.78rem;
            transition: background 0.15s;
        }

        .example-chip:hover { background: #eef2ff; }

        #results { margin-top: 8px; }

        .loading {
            text-align: center;
            padding: 40px;
            color: white;
        }

        .spinner {
            display: inline-block;
            width: 40px;
            height: 40px;
            border: 4px solid rgba(255,255,255,0.3);
            border-top-color: white;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-bottom: 12px;
        }

        @keyframes spin { to { transform: rotate(360deg); } }

        .results-header {
            color: white;
            margin-bottom: 16px;
            font-size: 1rem;
            opacity: 0.9;
        }

        .resource-card {
            background: white;
            border-radius: 16px;
            padding: 22px 26px;
            margin-bottom: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
            transition: transform 0.15s, box-shadow 0.15s;
        }

        .resource-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        }

        .resource-card.food    { border-left-color: #48bb78; }
        .resource-card.shelter { border-left-color: #ed8936; }
        .resource-card.health  { border-left-color: #e53e3e; }
        .resource-card.mental  { border-left-color: #9f7aea; }
        .resource-card.job     { border-left-color: #4299e1; }
        .resource-card.childcare { border-left-color: #f6ad55; }

        .card-top {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 10px;
        }

        .resource-name {
            font-size: 1.15rem;
            font-weight: 700;
            color: #2d3748;
        }

        .category-badge {
            background: #f0f4ff;
            color: #667eea;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
            flex-shrink: 0;
        }

        .category-badge.food     { background: #f0fff4; color: #38a169; }
        .category-badge.shelter  { background: #fffaf0; color: #c05621; }
        .category-badge.health   { background: #fff5f5; color: #c53030; }
        .category-badge.mental   { background: #faf5ff; color: #6b46c1; }
        .category-badge.job      { background: #ebf8ff; color: #2b6cb0; }
        .category-badge.childcare { background: #fffff0; color: #b7791f; }

        .resource-desc {
            color: #718096;
            font-size: 0.9rem;
            line-height: 1.5;
            margin-bottom: 12px;
        }

        .resource-meta { display: flex; gap: 20px; flex-wrap: wrap; }

        .meta-item {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.82rem;
            color: #4a5568;
        }

        .meta-item svg { flex-shrink: 0; }

        .error-card {
            background: #fff5f5;
            border: 1px solid #fed7d7;
            border-radius: 12px;
            padding: 20px;
            color: #c53030;
            text-align: center;
        }

        footer {
            text-align: center;
            color: rgba(255,255,255,0.6);
            font-size: 0.8rem;
            padding: 30px 0 20px;
        }

        footer a { color: rgba(255,255,255,0.8); }

        @media (max-width: 600px) {
            header h1 { font-size: 2rem; }
            .search-card { padding: 20px; }
            .form-row { flex-direction: column; }
        }
    </style>
</head>
<body>
<div class="container">
    <header>
        <h1>Community<span>AI</span></h1>
        <p>Find local food banks, shelters, clinics &amp; social services &mdash; instantly.</p>
        <div class="badge">Powered by OpenAI GPT-3.5</div>
    </header>

    <div class="search-card">
        <h2>What do you need help with?</h2>
        <form id="searchForm">
            <div class="form-row">
                <div class="form-group" style="flex:2">
                    <label for="query">Describe your need</label>
                    <input type="text" id="query" name="query"
                        placeholder="e.g. emergency food assistance for family of 4"
                        required autocomplete="off">
                </div>
                <div class="form-group" style="flex:1">
                    <label for="location">City or ZIP Code</label>
                    <input type="text" id="location" name="location"
                        placeholder="e.g. Chicago, IL" required autocomplete="off">
                </div>
            </div>
            <button type="submit" class="btn-search" id="searchBtn">
                Find Resources
            </button>
        </form>
        <div class="examples">
            <span>Try:</span>
            <span class="example-chip" onclick="fillExample('food bank', 'Detroit, MI')">food bank Detroit</span>
            <span class="example-chip" onclick="fillExample('homeless shelter tonight', 'Los Angeles, CA')">shelter LA</span>
            <span class="example-chip" onclick="fillExample('free mental health counseling', 'New York, NY')">mental health NYC</span>
            <span class="example-chip" onclick="fillExample('free dental clinic', 'Houston, TX')">dental Houston</span>
            <span class="example-chip" onclick="fillExample('job training programs', 'Atlanta, GA')">job training Atlanta</span>
        </div>
    </div>

    <div id="results"></div>

    <footer>
        Built for <a href="https://devdash.devpost.com" target="_blank">Dev_Dash 2026</a> &mdash;
        Theme: Code the Tomorrow &mdash;
        <a href="https://github.com/muhibwqr/communityai-resource-finder" target="_blank">GitHub</a>
    </footer>
</div>

<script>
function fillExample(query, location) {
    document.getElementById('query').value = query;
    document.getElementById('location').value = location;
    document.getElementById('searchForm').dispatchEvent(new Event('submit'));
}

function getCategoryClass(category) {
    if (!category) return '';
    const c = category.toLowerCase();
    if (c.includes('food') || c.includes('meal') || c.includes('nutrition')) return 'food';
    if (c.includes('shelter') || c.includes('housing') || c.includes('homeless')) return 'shelter';
    if (c.includes('health') || c.includes('clinic') || c.includes('medical') || c.includes('dental')) return 'health';
    if (c.includes('mental') || c.includes('counsel') || c.includes('therapy')) return 'mental';
    if (c.includes('job') || c.includes('employ') || c.includes('workforce')) return 'job';
    if (c.includes('child') || c.includes('family') || c.includes('youth')) return 'childcare';
    return '';
}

document.getElementById('searchForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const query = document.getElementById('query').value.trim();
    const location = document.getElementById('location').value.trim();
    const btn = document.getElementById('searchBtn');
    const resultsDiv = document.getElementById('results');

    btn.disabled = true;
    btn.textContent = 'Searching...';
    resultsDiv.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Finding resources in <strong>${location}</strong>...</p>
        </div>`;

    try {
        const resp = await fetch('/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, location })
        });
        const data = await resp.json();

        if (!resp.ok || data.error) {
            resultsDiv.innerHTML = `<div class="error-card"><strong>Error:</strong> ${data.error || 'Something went wrong. Please try again.'}</div>`;
            return;
        }

        const resources = data.resources;
        if (!resources || resources.length === 0) {
            resultsDiv.innerHTML = `<div class="error-card">No resources found. Try a broader search or different location.</div>`;
            return;
        }

        const catClass = r => getCategoryClass(r.category || '');
        resultsDiv.innerHTML = `
            <p class="results-header">Found <strong>${resources.length} resources</strong> near <strong>${location}</strong></p>
            ${resources.map(r => `
            <div class="resource-card ${catClass(r)}">
                <div class="card-top">
                    <div class="resource-name">${r.name || 'Unknown Resource'}</div>
                    <span class="category-badge ${catClass(r)}">${r.category || 'Resource'}</span>
                </div>
                <p class="resource-desc">${r.description || ''}</p>
                <div class="resource-meta">
                    ${r.address ? `<div class="meta-item"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>${r.address}</div>` : ''}
                    ${r.phone ? `<div class="meta-item"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.8a19.79 19.79 0 01-3.07-8.67A2 2 0 012 .84h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L6.09 8.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>${r.phone}</div>` : ''}
                    ${r.hours ? `<div class="meta-item"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>${r.hours}</div>` : ''}
                    ${r.website ? `<div class="meta-item"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/></svg><a href="${r.website}" target="_blank" style="color:#667eea">Website</a></div>` : ''}
                </div>
            </div>`).join('')}`;
    } catch (err) {
        resultsDiv.innerHTML = `<div class="error-card"><strong>Network error:</strong> ${err.message}</div>`;
    } finally {
        btn.disabled = false;
        btn.textContent = 'Find Resources';
    }
});
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/search", methods=["POST"])
def search():
    try:
        import openai
    except ImportError:
        return jsonify({"error": "openai package not installed. Run: pip install openai"}), 500

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    query = data.get("query", "").strip()
    location = data.get("location", "").strip()

    if not query or not location:
        return jsonify({"error": "Both query and location are required"}), 400

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return jsonify({"error": "OPENAI_API_KEY environment variable is not set"}), 500

    system_prompt = """You are a compassionate community resource assistant. Your job is to help people in need find local social services, food banks, shelters, clinics, and other community resources.

When given a need and a location, return a JSON object with a "resources" key containing an array of 5-8 relevant local resources. Each resource object must have these fields:
- name (string): Official name of the organization
- category (string): One of: Food Assistance, Homeless Shelter, Free Clinic, Mental Health, Job Training, Childcare, Financial Aid, Substance Abuse, Veterans Services, Senior Services, or other relevant category
- description (string): 1-2 sentence description of services offered
- address (string): Street address including city and state (use realistic addresses for the location)
- phone (string): Phone number in (XXX) XXX-XXXX format
- hours (string): Operating hours (e.g. "Mon-Fri 9AM-5PM")
- website (string or null): Website URL if available

Return ONLY valid JSON. No markdown, no explanation. Just the JSON object."""

    user_prompt = f"Need: {query}\nLocation: {location}\n\nFind local community resources that can help with this need in or near {location}."

    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=1500,
        )

        raw = response.choices[0].message.content.strip()

        # Strip markdown code fences if present
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

        result = json.loads(raw)
        if "resources" not in result:
            return jsonify({"error": "Unexpected response format from AI"}), 500

        return jsonify(result)

    except json.JSONDecodeError as e:
        return jsonify({"error": f"Failed to parse AI response: {str(e)}"}), 500
    except Exception as e:
        err_str = str(e)
        if "api_key" in err_str.lower() or "authentication" in err_str.lower():
            return jsonify({"error": "Invalid OpenAI API key. Please check your OPENAI_API_KEY."}), 401
        return jsonify({"error": f"AI service error: {err_str}"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    print(f"CommunityAI starting on http://localhost:{port}")
    print("Set OPENAI_API_KEY environment variable before running.")
    app.run(host="0.0.0.0", port=port, debug=debug)

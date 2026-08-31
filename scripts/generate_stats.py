import os
import json
import urllib.request
from datetime import datetime

def get_github_stats(username, token):
    """Fetch user stats from GitHub API."""
    stats = {
        'stars': 0,
        'followers': 0,
        'repos': 0,
        'contributions': 0
    }
    
    # If no token, return placeholder data so the script doesn't crash during local testing
    if not token:
        print("No GITHUB_TOKEN found. Using placeholder data for SVG generation.")
        return {'stars': 404, 'followers': 1337, 'repos': 42, 'contributions': 9001}

    try:
        # GraphQL Query for user stats
        query = """
        query($login: String!) {
          user(login: $login) {
            repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
              totalCount
              nodes { stargazerCount }
            }
            followers { totalCount }
            contributionsCollection {
              contributionCalendar { totalContributions }
            }
          }
        }
        """
        
        req = urllib.request.Request('https://api.github.com/graphql', method='POST')
        req.add_header('Authorization', f'Bearer {token}')
        req.add_header('Content-Type', 'application/json')
        data = json.dumps({'query': query, 'variables': {'login': username}}).encode('utf-8')
        
        with urllib.request.urlopen(req, data=data) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            user_data = result.get('data', {}).get('user', {})
            if user_data:
                repos = user_data.get('repositories', {})
                stats['repos'] = repos.get('totalCount', 0)
                stats['stars'] = sum(node.get('stargazerCount', 0) for node in repos.get('nodes', []))
                stats['followers'] = user_data.get('followers', {}).get('totalCount', 0)
                stats['contributions'] = user_data.get('contributionsCollection', {}).get('contributionCalendar', {}).get('totalContributions', 0)
    except Exception as e:
        print(f"Error fetching data: {e}")
        
    return stats

def generate_svg(stats, username):
    """Generate a highly beautified Liquid Morphism + Dot Matrix SVG."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 240" width="500" height="240">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DotGothic16&amp;family=VT323&amp;display=swap');
      .title {{ font-family: 'DotGothic16', monospace; font-size: 22px; fill: #e5e7eb; letter-spacing: 2px; }}
      .stat-label {{ font-family: 'VT323', monospace; font-size: 18px; fill: #9ca3af; }}
      .stat-value {{ font-family: 'DotGothic16', monospace; font-size: 24px; fill: #00d4ff; text-shadow: 0 0 5px rgba(0,212,255,0.5); }}
      .card {{ fill: rgba(10, 10, 10, 0.6); stroke: rgba(0, 212, 255, 0.3); stroke-width: 1.5; backdrop-filter: blur(15px); }}
    </style>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090979" />
      <stop offset="100%" stop-color="#00d4ff" />
    </linearGradient>
    <filter id="blur-filter" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="30" />
    </filter>
  </defs>

  <!-- Deep Black Background -->
  <rect width="500" height="240" fill="#050505" rx="15" />
  
  <!-- Subtle Grid -->
  <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
    <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#ffffff" stroke-width="0.5" opacity="0.05" />
  </pattern>
  <rect width="500" height="240" fill="url(#grid)" rx="15" />

  <!-- Liquid Blob (Animated, Glowing) -->
  <g transform="translate(400, 120)">
    <path fill="url(#grad1)" opacity="0.5" filter="url(#blur-filter)"
          d="M 60 -50 C 90 -20, 100 40, 70 70 C 40 100, -20 90, -50 60 C -80 30, -70 -30, -40 -60 C -10 -90, 30 -80, 60 -50 Z">
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="20s" repeatCount="indefinite"/>
    </path>
  </g>

  <!-- Premium Glassmorphism Card -->
  <rect x="20" y="20" width="460" height="200" rx="12" class="card" />
  
  <!-- Terminal Window Controls -->
  <circle cx="40" cy="40" r="5" fill="#ff5f56" />
  <circle cx="60" cy="40" r="5" fill="#ffbd2e" />
  <circle cx="80" cy="40" r="5" fill="#27c93f" />

  <!-- Header Text -->
  <text x="40" y="75" class="title"><tspan fill="#27c93f">root@kali</tspan><tspan fill="#e5e7eb">:~# ./sys_telemetry</tspan></text>
  
  <!-- Divider Line -->
  <line x1="40" y1="90" x2="460" y2="90" stroke="#333" stroke-width="1" stroke-dasharray="4" />

  <!-- Stat Rows with Fake "Progress Bars" for Hacker Aesthetic -->
  <text x="40" y="125" class="stat-label">Total Stars:</text>
  <text x="180" y="125" class="stat-value">{stats['stars']}</text>
  <rect x="250" y="115" width="190" height="8" fill="#111" rx="4" />
  <rect x="250" y="115" width="140" height="8" fill="#ff5f56" rx="4" />
  
  <text x="40" y="155" class="stat-label">Commits (1Y):</text>
  <text x="180" y="155" class="stat-value">{stats['contributions']}</text>
  <rect x="250" y="145" width="190" height="8" fill="#111" rx="4" />
  <rect x="250" y="145" width="170" height="8" fill="#27c93f" rx="4" />
  
  <text x="40" y="185" class="stat-label">Repositories:</text>
  <text x="180" y="185" class="stat-value">{stats['repos']}</text>
  <rect x="250" y="175" width="190" height="8" fill="#111" rx="4" />
  <rect x="250" y="175" width="100" height="8" fill="#00d4ff" rx="4" />

</svg>"""
    
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(repo_root, 'stats.svg')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(svg_template)
    print(f"Successfully generated {out_path}")

if __name__ == "__main__":
    username = os.environ.get("GITHUB_REPOSITORY_OWNER", "lingeshkumar-ctrl")
    token = os.environ.get("GITHUB_TOKEN", "")
    
    stats = get_github_stats(username, token)
    generate_svg(stats, username)

def create_results_html(self, results):
    """Create HTML page for search results with images and videos"""
    query = results.get('query', '')
    total = results.get('total', 0)
    search_time = results.get('search_time_ms', 0)
    results_list = results.get('results', [])
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Search: {query}</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; }}
            .result {{ margin: 25px 0; padding: 20px; border-bottom: 1px solid #eee; }}
            .title {{ color: #1a0dab; font-size: 18px; text-decoration: none; }}
            .title:hover {{ text-decoration: underline; }}
            .url {{ color: #006621; font-size: 14px; }}
            .snippet {{ color: #545454; font-size: 14px; margin-top: 5px; }}
            .stats {{ color: #666; font-size: 13px; margin-bottom: 20px; }}
            .media-container {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; }}
            .media-item {{ max-width: 150px; border-radius: 8px; overflow: hidden; }}
            .media-item img {{ width: 100%; height: auto; }}
            .media-item video {{ width: 100%; height: auto; }}
            .media-label {{ font-size: 11px; color: #888; display: block; }}
            .score {{ color: #999; font-size: 12px; }}
            .dark-mode {{ background: #1a1a1a; color: #e0e0e0; }}
            .dark-mode .title {{ color: #8ab4f8; }}
            .dark-mode .url {{ color: #bdc1c6; }}
            .dark-mode .snippet {{ color: #e0e0e0; }}
            .dark-mode .stats {{ color: #9aa0a6; }}
            .dark-mode .result {{ border-color: #444; }}
            .dark-mode .media-label {{ color: #888; }}
        </style>
    </head>
    <body>
        <h1>🔍 Search Results for "{query}"</h1>
        <div class="stats">About {total} results ({search_time} ms)</div>
    """
    
    for result in results_list:
        title = result.get('title', 'No title')
        url = result.get('url', '#')
        snippet = result.get('snippet', 'No description')
        score = result.get('score', 0)
        images = result.get('images', [])
        videos = result.get('videos', [])
        
        html += f"""
        <div class="result">
            <a class="title" href="{url}">{title}</a>
            <div class="url">{url}</div>
            <div class="snippet">{snippet}</div>
        """
        
        # Add images
        if images:
            html += '<div class="media-container">'
            for img in images[:4]:  # Limit to 4 images
                img_url = img.get('url', '')
                if img_url:
                    html += f'''
                    <div class="media-item">
                        <img src="{img_url}" alt="{img.get('alt', '')}" loading="lazy" onerror="this.style.display='none'">
                        <span class="media-label">🖼️ Image</span>
                    </div>
                    '''
            html += '</div>'
        
        # Add videos
        if videos:
            html += '<div class="media-container">'
            for video_url in videos[:2]:  # Limit to 2 videos
                if 'youtube.com' in video_url or 'youtu.be' in video_url:
                    # YouTube embed
                    video_id = video_url.split('v=')[-1] if 'v=' in video_url else video_url.split('/')[-1]
                    embed_url = f"https://www.youtube.com/embed/{video_id}"
                    html += f'''
                    <div class="media-item">
                        <iframe width="200" height="113" src="{embed_url}" frameborder="0" allowfullscreen></iframe>
                        <span class="media-label">🎬 YouTube</span>
                    </div>
                    '''
                else:
                    html += f'''
                    <div class="media-item">
                        <video width="200" controls>
                            <source src="{video_url}">
                            Your browser does not support video.
                        </video>
                        <span class="media-label">🎬 Video</span>
                    </div>
                    '''
            html += '</div>'
        
        html += f'<div class="score">Score: {score}</div>'
        html += '</div>'
    
    html += """
    </body>
    </html>
    """
    return html
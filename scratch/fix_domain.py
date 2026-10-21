import re

with open('templates/domain.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('<style>')
end_idx = content.find('</style>')

if start_idx != -1 and end_idx != -1:
    style_content = content[start_idx + len('<style>'):end_idx].strip()
    
    # Remove style block from domain.html
    new_domain_content = content[:start_idx] + '\n    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/style.css\') }}">\n' + content[end_idx + len('</style>'):]
    
    # Insert 4 domains
    new_domains_html = """
            <!-- =====================
                 FARMER
            ====================== -->
            <div class="domain-card reader">
                <div class="icon-circle">
                    <i class="fa-solid fa-tractor"></i>
                </div>
                <h3>Farmer</h3>
                <p>Latest farming, agriculture, and crop news</p>
                <a href="{{ url_for('index', domain='farmer') }}" class="arrow-btn">
                    <i class="fa-solid fa-arrow-right"></i>
                </a>
            </div>

            <!-- =====================
                 SPORTS FAN
            ====================== -->
            <div class="domain-card investor">
                <div class="icon-circle">
                    <i class="fa-solid fa-basketball"></i>
                </div>
                <h3>Sports Fan</h3>
                <p>Sports updates, scores, and news</p>
                <a href="{{ url_for('index', domain='sports_fan') }}" class="arrow-btn">
                    <i class="fa-solid fa-arrow-right"></i>
                </a>
            </div>

            <!-- =====================
                 POLITICIAN
            ====================== -->
            <div class="domain-card job">
                <div class="icon-circle">
                    <i class="fa-solid fa-landmark"></i>
                </div>
                <h3>Politician</h3>
                <p>Political news, government updates, and policies</p>
                <a href="{{ url_for('index', domain='politician') }}" class="arrow-btn">
                    <i class="fa-solid fa-arrow-right"></i>
                </a>
            </div>

            <!-- =====================
                 RESEARCHER
            ====================== -->
            <div class="domain-card engineer">
                <div class="icon-circle">
                    <i class="fa-solid fa-microscope"></i>
                </div>
                <h3>Researcher</h3>
                <p>Latest research papers, studies, and discoveries</p>
                <a href="{{ url_for('index', domain='researcher') }}" class="arrow-btn">
                    <i class="fa-solid fa-arrow-right"></i>
                </a>
            </div>
"""
    new_domain_content = new_domain_content.replace('    </div>\n\n\n        </div>\n\n    </main>', '    </div>\n' + new_domains_html + '\n\n        </div>\n\n    </main>')

    with open('templates/domain.html', 'w', encoding='utf-8') as f:
        f.write(new_domain_content)
        
    with open('static/css/style.css', 'a', encoding='utf-8') as f:
        f.write('\n\n/* =========================================\n')
        f.write('   DOMAIN PAGE STYLES (Moved from domain.html)\n')
        f.write('========================================= */\n\n')
        f.write(style_content)
        
    print('Style moved and domains added successfully!')
else:
    print('Style block not found in domain.html')

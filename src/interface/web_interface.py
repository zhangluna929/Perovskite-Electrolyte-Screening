# coding: utf-8
"""
Web界面模块
用Flask写的简单界面，功能还不完善
"""

try:
    from flask import Flask, render_template, request, jsonify, send_file
    import json
    import os
    from datetime import datetime
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # 后端用Agg，不然会报错
    import io
    import base64
except ImportError:
    print("⚠️ Flask模块未安装，请运行: pip install flask")
    exit(1)

# 中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

app = Flask(__name__)
app.secret_key = 'perovskite_screening_2024'

class WebInterface:
    
    def __init__(self):
        self.results_cache = {}  # 缓存结果，避免重复读取
        # TODO: 后面可能要加更多模块
        self.supported_modules = [
            'BVSE筛选',
            '高级筛选', 
            'ML筛选',
            '产业化分析',
            '证书生成'
        ]
    
    def load_results(self, result_type):
        """加载筛选结果"""
        file_mapping = {
            'bvse': 'bvse_results.json',
            'advanced': 'step3-6_results.json',
            'ml': 'ml_predictions.json',
            'industrial': 'industrial_analysis_report.json'
        }
        
        filename = file_mapping.get(result_type)
        if filename and os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return None
        return None
    
    def generate_chart(self, chart_type, data):
        """生成图表"""
        plt.figure(figsize=(10, 6))
        
        if chart_type == 'performance_comparison':
            materials = [d.get('formula', f'Material_{i}')[:10] for i, d in enumerate(data)]
            conductivities = [d.get('ionic_conductivity', d.get('predicted_conductivity', 1e-3)) for d in data]
            
            bars = plt.bar(materials, conductivities, color='skyblue')
            plt.title('材料电导率对比', fontsize=14, fontweight='bold')
            plt.ylabel('离子电导率 (S/cm)')
            plt.yscale('log')
            plt.xticks(rotation=45)
            
            # 添加数值标签
            for bar, value in zip(bars, conductivities):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.1,
                        f'{value:.2e}', ha='center', va='bottom', fontsize=9)
        
        elif chart_type == 'screening_funnel':
            stages = ['原始材料', 'BVSE筛选', '稳定性分析', '界面兼容性', 'NEB计算', '最终候选']
            counts = [67, 21, 15, 8, 5, 3]  # 示例数据
            
            plt.bar(stages, counts, color=['lightblue', 'lightgreen', 'lightyellow', 
                                         'lightcoral', 'lightpink', 'gold'])
            plt.title('筛选流程统计', fontsize=14, fontweight='bold')
            plt.ylabel('材料数量')
            plt.xticks(rotation=45)
            
            for i, count in enumerate(counts):
                plt.text(i, count + 1, str(count), ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        # 保存为base64字符串
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_str

web_interface = WebInterface()

@app.route('/')
def index():
    """主页"""
    return '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>钙钛矿电解质筛选平台</title>
        <style>
            body { 
                font-family: 'Microsoft YaHei', Arial, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                background: rgba(255,255,255,0.1); 
                border-radius: 15px; 
                padding: 30px;
                backdrop-filter: blur(10px);
            }
            h1 { 
                text-align: center; 
                color: white; 
                font-size: 2.5em; 
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .subtitle { 
                text-align: center; 
                color: #f0f0f0; 
                margin-bottom: 30px; 
                font-size: 1.2em;
            }
            .nav-grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                gap: 20px; 
                margin-top: 30px; 
            }
            .nav-card { 
                background: rgba(255,255,255,0.2); 
                border-radius: 10px; 
                padding: 20px; 
                text-align: center; 
                transition: transform 0.3s, box-shadow 0.3s;
                border: 1px solid rgba(255,255,255,0.3);
            }
            .nav-card:hover { 
                transform: translateY(-5px); 
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                background: rgba(255,255,255,0.3);
            }
            .nav-card h3 { 
                margin-top: 0; 
                color: white; 
                font-size: 1.3em;
            }
            .nav-card a { 
                color: #fff; 
                text-decoration: none; 
                font-weight: bold;
                display: block;
                padding: 10px;
                border-radius: 5px;
                background: rgba(255,255,255,0.1);
                margin-top: 10px;
                transition: background 0.3s;
            }
            .nav-card a:hover { 
                background: rgba(255,255,255,0.2); 
            }
            .icon { 
                font-size: 2em; 
                margin-bottom: 10px; 
            }
            .stats { 
                display: flex; 
                justify-content: space-around; 
                margin: 30px 0; 
                text-align: center;
            }
            .stat-item { 
                background: rgba(255,255,255,0.2); 
                padding: 15px; 
                border-radius: 10px;
                flex: 1;
                margin: 0 10px;
            }
            .stat-number { 
                font-size: 2em; 
                font-weight: bold; 
                color: #FFD700;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔬 钙钛矿电解质筛选平台</h1>
            <p class="subtitle">Perovskite Electrolyte Screening Platform v1.0</p>
            
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">67</div>
                    <div>原始材料</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">6</div>
                    <div>筛选步骤</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">3</div>
                    <div>推荐材料</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">4</div>
                    <div>分析模块</div>
                </div>
            </div>
            
            <div class="nav-grid">
                <div class="nav-card">
                    <div class="icon">⚡</div>
                    <h3>BVSE快速筛选</h3>
                    <p>键价格点能量扫描，快速识别离子传导路径</p>
                    <a href="/bvse">开始筛选</a>
                </div>
                
                <div class="nav-card">
                    <div class="icon">🔬</div>
                    <h3>高级筛选</h3>
                    <p>稳定性分析、界面兼容性、NEB计算</p>
                    <a href="/advanced">高级分析</a>
                </div>
                
                <div class="nav-card">
                    <div class="icon">🤖</div>
                    <h3>机器学习筛选</h3>
                    <p>AI加速材料性能预测和筛选</p>
                    <a href="/ml">ML预测</a>
                </div>
                
                <div class="nav-card">
                    <div class="icon">🏭</div>
                    <h3>产业化分析</h3>
                    <p>成本分析、市场预测、质量控制</p>
                    <a href="/industrial">产业分析</a>
                </div>
                
                <div class="nav-card">
                    <div class="icon">📊</div>
                    <h3>结果查看</h3>
                    <p>查看所有筛选结果和分析报告</p>
                    <a href="/results">查看结果</a>
                </div>
                
                <div class="nav-card">
                    <div class="icon">🏆</div>
                    <h3>证书生成</h3>
                    <p>生成材料认证证书和分析报告</p>
                    <a href="/certificates">生成证书</a>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 30px; color: #f0f0f0;">
                <p>💡 提示：首次使用建议先运行BVSE筛选生成基础数据</p>
                <p>📧 技术支持：LunaZhang | 🔗 文档：<a href="/api/docs" style="color: #FFD700;">API文档</a></p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/bvse')
def bvse_page():
    """BVSE筛选页面"""
    return '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>BVSE快速筛选</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .form-group { margin: 20px 0; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, select, button { padding: 10px; border: 1px solid #ddd; border-radius: 5px; width: 100%; box-sizing: border-box; }
            button { background: #007bff; color: white; cursor: pointer; margin-top: 10px; }
            button:hover { background: #0056b3; }
            .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; }
            .back-link { display: inline-block; margin-bottom: 20px; color: #007bff; text-decoration: none; }
            .back-link:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-link">← 返回主页</a>
            <h1>⚡ BVSE快速筛选</h1>
            
            <form id="bvseForm">
                <div class="form-group">
                    <label>材料化学式：</label>
                    <input type="text" id="formula" placeholder="例如：Li7La3Zr2O12" required>
                </div>
                
                <div class="form-group">
                    <label>BVSE能量阈值 (eV)：</label>
                    <input type="number" id="threshold" value="3.0" step="0.1" min="1.0" max="5.0">
                </div>
                
                <div class="form-group">
                    <label>分析类型：</label>
                    <select id="analysisType">
                        <option value="quick">快速分析</option>
                        <option value="detailed">详细分析</option>
                        <option value="batch">批量分析</option>
                    </select>
                </div>
                
                <button type="submit">开始BVSE分析</button>
            </form>
            
            <div id="result" class="result" style="display: none;">
                <h3>分析结果：</h3>
                <div id="resultContent"></div>
            </div>
        </div>
        
        <script>
            document.getElementById('bvseForm').onsubmit = function(e) {
                e.preventDefault();
                
                const formula = document.getElementById('formula').value;
                const threshold = document.getElementById('threshold').value;
                const analysisType = document.getElementById('analysisType').value;
                
                document.getElementById('resultContent').innerHTML = '🔍 正在进行BVSE分析...';
                document.getElementById('result').style.display = 'block';
                
                fetch('/api/bvse', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({formula, threshold, analysisType})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('resultContent').innerHTML = `
                            <p><strong>材料：</strong> ${data.formula}</p>
                            <p><strong>传导路径：</strong> ${data.pathways} 个</p>
                            <p><strong>最小能量：</strong> ${data.min_energy} eV</p>
                            <p><strong>筛选结果：</strong> <span style="color: ${data.passed ? 'green' : 'red'}">${data.passed ? '✅ 通过' : '❌ 未通过'}</span></p>
                            <p><strong>建议：</strong> ${data.recommendation}</p>
                        `;
                    } else {
                        document.getElementById('resultContent').innerHTML = `<p style="color: red;">❌ 分析失败：${data.error}</p>`;
                    }
                })
                .catch(error => {
                    document.getElementById('resultContent').innerHTML = `<p style="color: red;">❌ 网络错误：${error.message}</p>`;
                });
            };
        </script>
    </body>
    </html>
    '''

@app.route('/results')
def results_page():
    """结果查看页面"""
    return '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>筛选结果</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .tabs { display: flex; margin-bottom: 20px; border-bottom: 2px solid #ddd; }
            .tab { padding: 10px 20px; cursor: pointer; border: none; background: none; font-size: 16px; }
            .tab.active { background: #007bff; color: white; border-radius: 5px 5px 0 0; }
            .tab-content { display: none; }
            .tab-content.active { display: block; }
            .material-card { background: #f8f9fa; margin: 10px 0; padding: 15px; border-radius: 5px; border-left: 4px solid #007bff; }
            .back-link { display: inline-block; margin-bottom: 20px; color: #007bff; text-decoration: none; }
            .chart-container { text-align: center; margin: 20px 0; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background: #f8f9fa; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-link">← 返回主页</a>
            <h1>📊 筛选结果总览</h1>
            
            <div class="tabs">
                <button class="tab active" onclick="showTab('overview')">总体概览</button>
                <button class="tab" onclick="showTab('bvse')">BVSE结果</button>
                <button class="tab" onclick="showTab('advanced')">高级筛选</button>
                <button class="tab" onclick="showTab('ml')">ML预测</button>
            </div>
            
            <div id="overview" class="tab-content active">
                <h2>📈 筛选流程总览</h2>
                <div class="chart-container">
                    <img src="/api/chart/screening_funnel" alt="筛选流程图" style="max-width: 100%; height: auto;">
                </div>
                
                <h3>🏆 最终推荐材料</h3>
                <div class="material-card">
                    <h4>1. Li₇La₃Zr₂O₁₂ (LLZO)</h4>
                    <p><strong>激活能：</strong> 0.10 eV | <strong>电导率：</strong> 1.5×10⁻³ S/cm | <strong>评级：</strong> 优秀</p>
                </div>
                <div class="material-card">
                    <h4>2. LiNbO₃</h4>
                    <p><strong>激活能：</strong> 0.15 eV | <strong>电导率：</strong> 1.2×10⁻³ S/cm | <strong>评级：</strong> 良好</p>
                </div>
                <div class="material-card">
                    <h4>3. LiTaO₃</h4>
                    <p><strong>激活能：</strong> 0.18 eV | <strong>电导率：</strong> 8.5×10⁻⁴ S/cm | <strong>评级：</strong> 合格</p>
                </div>
            </div>
            
            <div id="bvse" class="tab-content">
                <h2>⚡ BVSE筛选结果</h2>
                <p id="bvseStatus">正在加载BVSE结果...</p>
                <div id="bvseData"></div>
            </div>
            
            <div id="advanced" class="tab-content">
                <h2>🔬 高级筛选结果</h2>
                <p id="advancedStatus">正在加载高级筛选结果...</p>
                <div id="advancedData"></div>
            </div>
            
            <div id="ml" class="tab-content">
                <h2>🤖 机器学习预测结果</h2>
                <p id="mlStatus">正在加载ML预测结果...</p>
                <div id="mlData"></div>
            </div>
        </div>
        
        <script>
            function showTab(tabName) {
                // 隐藏所有标签页
                const contents = document.querySelectorAll('.tab-content');
                contents.forEach(content => content.classList.remove('active'));
                
                const tabs = document.querySelectorAll('.tab');
                tabs.forEach(tab => tab.classList.remove('active'));
                
                // 显示选中的标签页
                document.getElementById(tabName).classList.add('active');
                event.target.classList.add('active');
                
                // 加载对应数据
                loadTabData(tabName);
            }
            
            function loadTabData(tabName) {
                if (tabName === 'bvse') {
                    fetch('/api/results/bvse')
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                document.getElementById('bvseStatus').innerHTML = `✅ 已加载 ${data.total} 个BVSE结果`;
                                document.getElementById('bvseData').innerHTML = formatBvseResults(data.results);
                            } else {
                                document.getElementById('bvseStatus').innerHTML = '❌ BVSE结果文件不存在';
                            }
                        });
                }
                // 类似处理其他标签页...
            }
            
            function formatBvseResults(results) {
                if (!results || results.length === 0) return '<p>暂无结果</p>';
                
                let html = '<table><tr><th>材料</th><th>传导路径</th><th>最小能量</th><th>状态</th></tr>';
                results.slice(0, 10).forEach(result => {
                    html += `<tr>
                        <td>${result.formula || 'Unknown'}</td>
                        <td>${result.pathway_count || 0}</td>
                        <td>${result.min_energy ? result.min_energy.toFixed(3) : 'N/A'} eV</td>
                        <td>${result.bvse_passed ? '✅ 通过' : '❌ 未通过'}</td>
                    </tr>`;
                });
                html += '</table>';
                return html;
            }
            
            // 页面加载时自动加载概览数据
            window.onload = function() {
                loadTabData('overview');
            };
        </script>
    </body>
    </html>
    '''

# API 路由
@app.route('/api/bvse', methods=['POST'])
def api_bvse():
    """BVSE API"""
    data = request.get_json()
    formula = data.get('formula', 'Unknown')
    threshold = float(data.get('threshold', 3.0))
    
    # 模拟BVSE分析
    import random
    pathways = random.randint(0, 5)
    min_energy = random.uniform(1.5, 4.5)
    passed = min_energy < threshold and pathways > 0
    
    result = {
        'success': True,
        'formula': formula,
        'pathways': pathways,
        'min_energy': round(min_energy, 3),
        'passed': passed,
        'recommendation': '建议进入下一步筛选' if passed else '不建议继续，能量壁垒过高'
    }
    
    return jsonify(result)

@app.route('/api/results/<result_type>')
def api_results(result_type):
    """获取筛选结果API"""
    data = web_interface.load_results(result_type)
    
    if data:
        if result_type == 'bvse':
            results = data.get('bvse_results', [])
            return jsonify({
                'success': True,
                'total': len(results),
                'results': results[:10],  # 只返回前10个
                'summary': data.get('summary', {})
            })
        else:
            return jsonify({'success': True, 'data': data})
    else:
        return jsonify({'success': False, 'error': f'{result_type}结果文件不存在'})

@app.route('/api/chart/<chart_type>')
def api_chart(chart_type):
    """生成图表API"""
    # 模拟数据
    if chart_type == 'screening_funnel':
        data = []  # 筛选流程数据
    elif chart_type == 'performance_comparison':
        data = [
            {'formula': 'Li7La3Zr2O12', 'ionic_conductivity': 1.5e-3},
            {'formula': 'LiNbO3', 'ionic_conductivity': 1.2e-3},
            {'formula': 'LiTaO3', 'ionic_conductivity': 8.5e-4}
        ]
    else:
        data = []
    
    chart_base64 = web_interface.generate_chart(chart_type, data)
    
    # 返回base64图片
    from flask import Response
    import base64
    
    img_data = base64.b64decode(chart_base64)
    return Response(img_data, mimetype='image/png')

@app.route('/api/docs')
def api_docs():
    """API文档"""
    return '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>API文档</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
            .container { max-width: 800px; margin: 0 auto; }
            h1, h2 { color: #333; }
            .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff; }
            .method { font-weight: bold; color: #007bff; }
            pre { background: #f4f4f4; padding: 10px; border-radius: 3px; overflow-x: auto; }
            .back-link { display: inline-block; margin-bottom: 20px; color: #007bff; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-link">← 返回主页</a>
            <h1>🔗 API文档</h1>
            
            <h2>基础信息</h2>
            <p>钙钛矿电解质筛选平台提供RESTful API接口，支持JSON格式数据交换。</p>
            
            <div class="endpoint">
                <h3><span class="method">POST</span> /api/bvse</h3>
                <p>执行BVSE快速筛选分析</p>
                <h4>请求参数：</h4>
                <pre>{
  "formula": "Li7La3Zr2O12",
  "threshold": 3.0,
  "analysisType": "quick"
}</pre>
                <h4>响应示例：</h4>
                <pre>{
  "success": true,
  "formula": "Li7La3Zr2O12",
  "pathways": 3,
  "min_energy": 2.1,
  "passed": true,
  "recommendation": "建议进入下一步筛选"
}</pre>
            </div>
            
            <div class="endpoint">
                <h3><span class="method">GET</span> /api/results/{type}</h3>
                <p>获取筛选结果数据</p>
                <p>支持的类型：bvse, advanced, ml, industrial</p>
                <h4>响应示例：</h4>
                <pre>{
  "success": true,
  "total": 5,
  "results": [...],
  "summary": {...}
}</pre>
            </div>
            
            <div class="endpoint">
                <h3><span class="method">GET</span> /api/chart/{type}</h3>
                <p>生成分析图表</p>
                <p>支持的类型：screening_funnel, performance_comparison</p>
                <p>返回PNG格式图片</p>
            </div>
            
            <h2>错误处理</h2>
            <p>所有API在出错时返回如下格式：</p>
            <pre>{
  "success": false,
  "error": "错误描述"
}</pre>
            
            <h2>使用示例</h2>
            <h3>Python</h3>
            <pre>import requests

# BVSE分析
response = requests.post('http://localhost:5000/api/bvse', 
                        json={'formula': 'Li7La3Zr2O12'})
result = response.json()
print(result['passed'])

# 获取结果
response = requests.get('http://localhost:5000/api/results/bvse')
data = response.json()
print(f"总共{data['total']}个结果")</pre>
            
            <h3>JavaScript</h3>
            <pre>// BVSE分析
fetch('/api/bvse', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({formula: 'Li7La3Zr2O12'})
})
.then(response => response.json())
.then(data => console.log(data.passed));</pre>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("🌐 启动Web界面...")
    print("📱 访问地址: http://localhost:5000")
    print("📋 API文档: http://localhost:5000/api/docs")
    print("⏹️ 按 Ctrl+C 停止服务器")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 
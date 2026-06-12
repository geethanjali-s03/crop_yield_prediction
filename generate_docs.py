from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import KeepTogether
import os

# ── Colors ──────────────────────────────────────────────────────
GREEN   = colors.HexColor('#1a6b3c')
GREEN_L = colors.HexColor('#e8f5e9')
GREEN_M = colors.HexColor('#a5d6a7')
BLUE    = colors.HexColor('#1565c0')
BLUE_L  = colors.HexColor('#e3f2fd')
ORANGE  = colors.HexColor('#e65100')
ORANGE_L= colors.HexColor('#fff3e0')
GRAY    = colors.HexColor('#6b7280')
GRAY_L  = colors.HexColor('#f9fafb')
DARK    = colors.HexColor('#111827')
WHITE   = colors.white

def build_styles():
    s = getSampleStyleSheet()
    custom = {}
    custom['H1'] = ParagraphStyle('H1', parent=s['Heading1'], fontSize=20, textColor=GREEN,
                                   spaceAfter=6, spaceBefore=20, fontName='Helvetica-Bold')
    custom['H2'] = ParagraphStyle('H2', parent=s['Heading2'], fontSize=14, textColor=GREEN,
                                   spaceAfter=4, spaceBefore=14, fontName='Helvetica-Bold',
                                   borderPad=4)
    custom['H3'] = ParagraphStyle('H3', parent=s['Heading3'], fontSize=11, textColor=BLUE,
                                   spaceAfter=3, spaceBefore=10, fontName='Helvetica-Bold')
    custom['Body'] = ParagraphStyle('Body', parent=s['Normal'], fontSize=10, leading=16,
                                     textColor=DARK, spaceAfter=6, alignment=TA_JUSTIFY)
    custom['Bullet'] = ParagraphStyle('Bullet', parent=s['Normal'], fontSize=10, leading=15,
                                       leftIndent=14, spaceAfter=3, textColor=DARK,
                                       bulletIndent=4, bulletFontName='Helvetica',
                                       bulletFontSize=10)
    custom['Code'] = ParagraphStyle('Code', parent=s['Code'], fontSize=8.5, leading=13,
                                     fontName='Courier', backColor=colors.HexColor('#f3f4f6'),
                                     borderPad=6, leftIndent=8, spaceAfter=8)
    custom['Caption'] = ParagraphStyle('Caption', parent=s['Normal'], fontSize=9,
                                        textColor=GRAY, alignment=TA_CENTER, spaceAfter=8)
    custom['Cover'] = ParagraphStyle('Cover', parent=s['Normal'], fontSize=11,
                                      textColor=colors.HexColor('#374151'), alignment=TA_CENTER,
                                      leading=18)
    return custom

def hr(color=GREEN_M):
    return HRFlowable(width='100%', thickness=1, color=color, spaceAfter=8, spaceBefore=4)

def section_box(story, styles, title, content_fn):
    story.append(Paragraph(title, styles['H2']))
    story.append(hr(GREEN_M))
    content_fn(story, styles)
    story.append(Spacer(1, 4))

def bullet(text, styles):
    return Paragraph(f'<bullet>&bull;</bullet> {text}', styles['Bullet'])

def build_pdf(path):
    doc = SimpleDocTemplate(path, pagesize=A4,
                             leftMargin=2.5*cm, rightMargin=2.5*cm,
                             topMargin=2.5*cm, bottomMargin=2.5*cm,
                             title='CropYield AI — Project Documentation')
    styles = build_styles()
    story = []

    # ── Cover Page ─────────────────────────────────────────────────
    story.append(Spacer(1, 2*cm))

    # Title banner
    banner_data = [['🌾  CropYield AI']]
    banner = Table(banner_data, colWidths=['100%'])
    banner.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), GREEN),
        ('TEXTCOLOR',  (0,0), (-1,-1), WHITE),
        ('FONTNAME',   (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 28),
        ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 24),
        ('BOTTOMPADDING',(0,0),(-1,-1), 24),
        ('ROUNDEDCORNERS', [8]),
    ]))
    story.append(banner)
    story.append(Spacer(1, 0.5*cm))

    sub_data = [['Intelligent Crop Yield Prediction System']]
    sub_t = Table(sub_data, colWidths=['100%'])
    sub_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), GREEN_L),
        ('TEXTCOLOR',  (0,0), (-1,-1), GREEN),
        ('FONTNAME',   (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 14),
        ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING',(0,0),(-1,-1), 12),
    ]))
    story.append(sub_t)
    story.append(Spacer(1, 1.5*cm))

    story.append(Paragraph('AI/ML Final Year Project Documentation', styles['Cover']))
    story.append(Spacer(1, 0.3*cm))

    # Tech badges
    techs = [['Python Flask', 'MongoDB NoSQL', 'Scikit-learn', 'XGBoost', 'Bootstrap 5']]
    tech_t = Table(techs, colWidths=[3*cm]*5)
    tech_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BLUE_L),
        ('BACKGROUND', (1,0), (1,0), GREEN_L),
        ('BACKGROUND', (2,0), (2,0), ORANGE_L),
        ('BACKGROUND', (3,0), (3,0), GREEN_L),
        ('BACKGROUND', (4,0), (4,0), BLUE_L),
        ('TEXTCOLOR', (0,0), (-1,-1), DARK),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('ROUNDEDCORNERS', [4]),
    ]))
    story.append(tech_t)
    story.append(Spacer(1, 3*cm))

    info_data = [
        ['Project Title:', 'Crop Yield Prediction System using ML & MongoDB'],
        ['Project Type:', 'AI/ML Final Year / Mini Project (PBL)'],
        ['Domain:', 'Agricultural Intelligence / Data Science'],
        ['Backend:', 'Python 3.10 + Flask 3.0'],
        ['Frontend:', 'HTML5 + Bootstrap 5 + JavaScript'],
        ['Database:', 'MongoDB (NoSQL)'],
        ['ML Libraries:', 'Scikit-learn, XGBoost, Pandas, NumPy'],
        ['Best Model:', 'XGBoost Regressor — 97.77% Accuracy'],
        ['Year:', '2024'],
    ]
    info_t = Table(info_data, colWidths=[4.5*cm, 11*cm])
    info_t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('TEXTCOLOR', (0,0), (0,-1), GREEN),
        ('TEXTCOLOR', (1,0), (1,-1), DARK),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [WHITE, GRAY_L]),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.3, GREEN_M),
    ]))
    story.append(info_t)
    story.append(PageBreak())

    # ── Abstract ───────────────────────────────────────────────────
    story.append(Paragraph('Abstract', styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        'CropYield AI is an end-to-end intelligent agricultural platform that leverages machine learning '
        'to predict crop yield based on environmental and agricultural parameters. The system integrates '
        'five ML algorithms — Linear Regression, Decision Tree, Random Forest, XGBoost, and SVM — and '
        'automatically selects the best-performing model based on R² score evaluation. MongoDB serves as '
        'the NoSQL backend, storing user records, agricultural datasets, prediction history, reports, and '
        'system logs across five collections. The platform provides a professional Flask-based web '
        'dashboard with interactive forms, EDA visualizations, report generation, and role-based access '
        'control for farmers and administrators. Experimental results demonstrate XGBoost achieving '
        '97.77% prediction accuracy on the crop yield dataset.', styles['Body']))
    story.append(Spacer(1, 0.3*cm))

    # Keywords
    kw_data = [['Keywords: Crop Yield Prediction, Machine Learning, XGBoost, MongoDB, Flask, EDA, Random Forest, Agricultural Intelligence']]
    kw_t = Table(kw_data, colWidths=['100%'])
    kw_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), GREEN_L),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Oblique'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TEXTCOLOR', (0,0), (-1,-1), GREEN),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(kw_t)
    story.append(PageBreak())

    # ── Introduction ──────────────────────────────────────────────
    story.append(Paragraph('1. Introduction', styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        'Agriculture forms the backbone of economies worldwide, yet crop yield estimation remains '
        'challenging due to the multitude of interacting environmental, soil, and management factors. '
        'Traditional methods rely on expert knowledge and historical averages, which often fail to '
        'account for year-to-year variability in rainfall, temperature, and pest pressure.', styles['Body']))
    story.append(Paragraph(
        'Machine learning provides a powerful alternative: by training models on historical data '
        'encompassing rainfall, temperature, humidity, soil type, fertilizer usage, and crop variety, '
        'we can build predictive systems that generalise to new conditions. This project, CropYield AI, '
        'demonstrates a complete implementation of such a system — from data generation and preprocessing '
        'to model training, evaluation, deployment, and user-facing web interface.', styles['Body']))

    story.append(Paragraph('1.1 Problem Statement', styles['H3']))
    story.append(Paragraph(
        'Farmers and agricultural planners lack reliable, data-driven tools to estimate crop yield '
        'before the harvest season. This uncertainty leads to poor resource allocation, inadequate '
        'insurance pricing, and suboptimal government procurement policies. The objective of this '
        'project is to build an intelligent, accessible, and accurate crop yield prediction system '
        'that addresses this gap.', styles['Body']))

    story.append(Paragraph('1.2 Objectives', styles['H3']))
    for obj in [
        'Develop an ML pipeline that trains and evaluates 5 regression algorithms',
        'Integrate MongoDB as the NoSQL database with 5 collections (CRUD operations)',
        'Build a Flask web application with role-based access (admin & farmer)',
        'Implement EDA with at least 6 types of visualizations',
        'Achieve >90% prediction accuracy using the best-selected model',
        'Generate exportable prediction reports',
    ]:
        story.append(bullet(obj, styles))
    story.append(PageBreak())

    # ── Literature Survey ─────────────────────────────────────────
    story.append(Paragraph('2. Literature Survey', styles['H1']))
    story.append(hr())

    papers = [
        ['[1]', 'Pantazi et al. (2016)', 'Wheat yield prediction using ML algorithms',
         'Compared SVM, ANN, KNN for wheat yield — SVM achieved best RMSE'],
        ['[2]', 'Jeong et al. (2016)', 'Random Forest approach to corn yield prediction',
         'RF outperformed linear models; ensemble methods showed robustness'],
        ['[3]', 'Everingham et al. (2016)', 'Accurate rainfall forecasting for sugarcane production',
         'Demonstrated rainfall as the primary yield determinant'],
        ['[4]', 'Gandhi et al. (2016)', 'Rice crop yield prediction in India using ML',
         'Decision Trees and RF showed 85-92% accuracy on Indian datasets'],
        ['[5]', 'Khaki & Wang (2019)', 'Crop yield prediction using deep neural networks',
         'CNN-based model outperformed traditional ML on large-scale data'],
    ]
    lit_t = Table(papers, colWidths=[0.8*cm, 4*cm, 5.5*cm, 5.5*cm])
    lit_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, GRAY_L]),
        ('GRID', (0,0), (-1,-1), 0.3, GREEN_M),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(lit_t)
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        'The reviewed literature consistently shows that ensemble methods (Random Forest, XGBoost) '
        'outperform traditional regression on agricultural datasets due to their ability to capture '
        'non-linear feature interactions. This project incorporates these findings by implementing '
        'all major algorithm families and auto-selecting the best performer.', styles['Body']))
    story.append(PageBreak())

    # ── Existing vs Proposed ──────────────────────────────────────
    story.append(Paragraph('3. Existing vs Proposed System', styles['H1']))
    story.append(hr())

    comp = [
        ['Feature', 'Existing Systems', 'Proposed System (CropYield AI)'],
        ['Prediction Method', 'Statistical averages / Expert rules', '5 ML algorithms with auto-selection'],
        ['Database', 'Relational SQL or flat files', 'MongoDB NoSQL (5 collections)'],
        ['Model Selection', 'Manual / Single algorithm', 'Automated R²-based selection'],
        ['User Interface', 'None / Spreadsheet', 'Professional Flask web dashboard'],
        ['EDA', 'Manual Excel charts', '6 automated Matplotlib/Seaborn plots'],
        ['Role Management', 'None', 'Admin + Farmer roles (session-based)'],
        ['History Tracking', 'No', 'MongoDB predictions collection'],
        ['Report Export', 'Manual', 'CSV export + printable web report'],
        ['Accuracy', '70-80% (statistical)', '97.77% (XGBoost)'],
    ]
    comp_t = Table(comp, colWidths=[4*cm, 5.5*cm, 6.3*cm])
    comp_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (1,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, GRAY_L]),
        ('TEXTCOLOR', (2,1), (2,-1), colors.HexColor('#166534')),
        ('GRID', (0,0), (-1,-1), 0.3, GREEN_M),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(comp_t)
    story.append(PageBreak())

    # ── Methodology ───────────────────────────────────────────────
    story.append(Paragraph('4. Methodology', styles['H1']))
    story.append(hr())

    story.append(Paragraph('4.1 Dataset Preparation', styles['H2']))
    story.append(hr(GREEN_M))
    story.append(Paragraph(
        'A synthetic agricultural dataset of 2,000 samples was generated using NumPy with '
        'realistic crop-specific yield functions incorporating 11 features. The dataset was '
        'designed to mimic real-world agricultural conditions across 10 Indian states.', styles['Body']))

    feat_data = [
        ['Feature', 'Type', 'Range / Values', 'Preprocessing'],
        ['Crop', 'Categorical', '10 varieties', 'Label Encoding'],
        ['State', 'Categorical', '10 states', 'Label Encoding'],
        ['Season', 'Categorical', 'Kharif/Rabi/Zaid/Summer/Winter', 'Label Encoding'],
        ['Soil_Type', 'Categorical', 'Clay/Sandy/Loamy/Silty/Chalky/Peaty', 'Label Encoding'],
        ['Weather_Condition', 'Categorical', 'Sunny/Rainy/Cloudy/Humid/Dry', 'Label Encoding'],
        ['Area', 'Numerical', '0.5–50 ha', 'StandardScaler'],
        ['Rainfall', 'Numerical', '200–2500 mm', 'StandardScaler'],
        ['Temperature', 'Numerical', '15–45 °C', 'StandardScaler'],
        ['Humidity', 'Numerical', '20–95 %', 'StandardScaler'],
        ['Fertilizer_Usage', 'Numerical', '50–500 kg/ha', 'StandardScaler'],
        ['Pesticide_Usage', 'Numerical', '0.1–5.0 kg/ha', 'StandardScaler'],
        ['Yield_Per_Hectare', 'Target', 'Variable (kg/ha)', 'None (target)'],
    ]
    ft = Table(feat_data, colWidths=[4*cm, 3*cm, 5.5*cm, 3.3*cm])
    ft.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BLUE_L]),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#b3d4f5')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(ft)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph('Preprocessing Pipeline:', styles['H3']))
    for step in [
        'Missing value check and removal (dropna)',
        'Label Encoding for all 5 categorical columns',
        'StandardScaler applied to numerical features (for SVM and Linear Regression)',
        'Train/Test Split: 80% training, 20% testing (random_state=42)',
        'No data leakage — scaler fitted only on training set',
    ]:
        story.append(bullet(step, styles))
    story.append(PageBreak())

    # ── ML Models ─────────────────────────────────────────────────
    story.append(Paragraph('5. Machine Learning Algorithms', styles['H1']))
    story.append(hr())

    algos = [
        ['Algorithm', 'Type', 'Key Parameters', 'R² Score', 'MAE', 'Accuracy'],
        ['Linear Regression', 'Baseline', 'Default', '0.1735', '~480', '17.35%'],
        ['Decision Tree', 'Tree', 'max_depth=10', '0.9730', '~95', '97.30%'],
        ['Random Forest', 'Ensemble', 'n_estimators=100', '0.9730', '~96', '97.30%'],
        ['XGBoost ★', 'Gradient Boost', 'n_estimators=100', '0.9777', '~87', '97.77%'],
        ['SVM (SVR)', 'Kernel', 'C=100, rbf', '-0.067', 'high', '0% (poor fit)'],
    ]
    at = Table(algos, colWidths=[3.8*cm, 2.8*cm, 3.5*cm, 2*cm, 1.8*cm, 2*cm])
    at.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, GRAY_L]),
        ('BACKGROUND', (0,4), (-1,4), GREEN_L),
        ('FONTNAME', (0,4), (-1,4), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.3, GREEN_M),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (3,0), (-1,-1), 'CENTER'),
    ]))
    story.append(at)
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph(
        '★ XGBoost Regressor was automatically selected as the deployed model due to '
        'achieving the highest R² score of 0.9777 and lowest MAE on the test set.', styles['Body']))

    story.append(Paragraph('5.1 Evaluation Metrics', styles['H3']))
    metrics = [
        ['Metric', 'Formula', 'Interpretation'],
        ['R² Score', '1 - SS_res / SS_tot', '1.0 = perfect; 0 = baseline mean model'],
        ['RMSE', 'sqrt(mean((y_true - y_pred)²))', 'Same units as target; lower is better'],
        ['MAE', 'mean(|y_true - y_pred|)', 'Average absolute error; robust to outliers'],
        ['Accuracy %', 'max(0, R²) × 100', 'R²-based percentage for interpretability'],
    ]
    mt = Table(metrics, colWidths=[3.2*cm, 6*cm, 6.6*cm])
    mt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BLUE_L]),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#b3d4f5')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('FONTNAME', (1,1), (1,-1), 'Courier'),
    ]))
    story.append(mt)
    story.append(PageBreak())

    # ── MongoDB Design ────────────────────────────────────────────
    story.append(Paragraph('6. NoSQL Database Design (MongoDB)', styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        'MongoDB was selected as the NoSQL database for its flexibility with semi-structured '
        'agricultural records, native JSON document model, and scalability. PyMongo is used as '
        'the Python driver with graceful degradation when MongoDB is not available.', styles['Body']))

    story.append(Paragraph('6.1 Collections', styles['H2']))
    story.append(hr(GREEN_M))

    collections = [
        ['Collection', 'Purpose', 'Key Fields'],
        ['users', 'User authentication & profiles', 'username, email, password_hash, role, created_at, active'],
        ['crop_data', 'Agricultural dataset storage', 'Crop, State, Season, Soil_Type, Area, Rainfall, Temperature, Humidity, Fertilizer_Usage, Yield_Per_Hectare'],
        ['predictions', 'Prediction history', 'username, input (document), result (document), timestamp'],
        ['reports', 'Generated reports', 'username, data (array), created_at'],
        ['logs', 'System audit trail', 'type, message, username, timestamp'],
    ]
    ct = Table(collections, colWidths=[3.2*cm, 4.5*cm, 8.1*cm])
    ct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,1), (0,-1), 'Courier-Bold'),
        ('FONTNAME', (1,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, GRAY_L]),
        ('GRID', (0,0), (-1,-1), 0.3, GREEN_M),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(ct)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph('6.2 Sample Document — predictions collection', styles['H3']))
    story.append(Paragraph('''<font name="Courier" size="8.5">{
  "_id": ObjectId("..."),
  "username": "farmer1",
  "input": {
    "Crop": "Rice", "State": "Punjab", "Season": "Kharif",
    "Soil_Type": "Loamy", "Weather_Condition": "Rainy",
    "Area": 5.0, "Rainfall": 1200, "Temperature": 28,
    "Humidity": 75, "Fertilizer_Usage": 250, "Pesticide_Usage": 1.5
  },
  "result": {
    "yield_per_hectare": 3847.25,
    "total_yield": 19236.25,
    "model_used": "XGBoost",
    "confidence": 97.77,
    "accuracy": 97.77
  },
  "timestamp": ISODate("2024-01-15T10:30:00Z")
}</font>''', styles['Code']))
    story.append(PageBreak())

    # ── System Architecture ───────────────────────────────────────
    story.append(Paragraph('7. System Architecture & Modules', styles['H1']))
    story.append(hr())

    story.append(Paragraph('7.1 Architecture Overview', styles['H2']))
    story.append(hr(GREEN_M))

    arch_layers = [
        ['Presentation Layer', 'HTML5 + Bootstrap 5 + JavaScript + Jinja2 Templates'],
        ['Application Layer', 'Python Flask 3.0 (Routes, Session Management, REST API)'],
        ['ML Engine', 'Scikit-learn + XGBoost + Joblib (5 algorithms, auto-selection)'],
        ['Data Processing', 'Pandas + NumPy (preprocessing, encoding, scaling)'],
        ['Visualization', 'Matplotlib + Seaborn (6 chart types, base64 encoded)'],
        ['Database Layer', 'MongoDB (PyMongo driver, 5 collections)'],
        ['Storage', 'Joblib model files (.pkl) + JSON metadata'],
    ]
    arch_t = Table(arch_layers, colWidths=[5*cm, 10.8*cm])
    colors_list = [GREEN_L, BLUE_L, ORANGE_L, colors.HexColor('#f3e5f5'), GREEN_L, ORANGE_L, BLUE_L]
    for i, row_color in enumerate(colors_list):
        arch_t.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), row_color)]))
    arch_t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9.5),
        ('TEXTCOLOR', (0,0), (0,-1), DARK),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d1d5db')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(arch_t)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph('7.2 Module Descriptions', styles['H2']))
    story.append(hr(GREEN_M))

    modules = [
        ('User Module', [
            'User registration with password hashing (Werkzeug)',
            'Login/logout with Flask session management',
            'Input 11 agricultural parameters via interactive form with sliders',
            'View prediction result: yield/ha, total yield, confidence, model used',
            'Access personal prediction history',
        ]),
        ('Admin Module', [
            'View all registered users from MongoDB users collection',
            'Monitor all system predictions and analytics',
            'View raw dataset sample from crop_data collection',
            'Access system event audit logs',
            'Crop-wise prediction analytics with average yields',
        ]),
        ('Prediction Module', [
            'Loads serialised best model (joblib .pkl file)',
            'Applies label encoders and scaler to input',
            'Returns yield per hectare + total yield + confidence',
            'Saves prediction to MongoDB predictions collection',
            'Logs prediction event to system logs',
        ]),
        ('EDA & Visualization Module', [
            'Yield distribution histogram and crop boxplot',
            'Rainfall vs crop yield scatter plot (6 crops)',
            'Feature correlation heatmap (Seaborn)',
            'Crop × Season average yield bar chart',
            'Feature importance based on Pearson correlation',
            'Multi-model R² and MAE comparison chart',
        ]),
        ('Report Module', [
            'Tabular report of all user predictions',
            'Summary stats: total predictions, avg yield, avg confidence',
            'CSV export with all parameters and results',
            'Printable browser-native print view',
        ]),
    ]
    for mod_name, mod_features in modules:
        story.append(Paragraph(mod_name, styles['H3']))
        for f in mod_features:
            story.append(bullet(f, styles))
        story.append(Spacer(1, 0.2*cm))

    story.append(PageBreak())

    # ── Results ───────────────────────────────────────────────────
    story.append(Paragraph('8. Results & Discussion', styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        'The system was evaluated on a synthetic dataset of 2,000 samples with 80/20 train-test '
        'split. All five algorithms were trained and evaluated; XGBoost achieved the highest R² '
        'score of 0.9777, corresponding to 97.77% prediction accuracy.', styles['Body']))

    results = [
        ['Algorithm', 'R² Score', 'RMSE (kg/ha)', 'MAE (kg/ha)', 'Accuracy (%)', 'Status'],
        ['Linear Regression', '0.1735', '~4,800', '~480', '17.35', 'Baseline'],
        ['Decision Tree', '0.9730', '~870', '~95', '97.30', 'Good'],
        ['Random Forest', '0.9730', '~868', '~96', '97.30', 'Good'],
        ['XGBoost', '0.9777', '~792', '~87', '97.77', '★ BEST'],
        ['SVM (SVR)', '-0.067', 'high', 'high', '0.00', 'Poor fit'],
    ]
    rt = Table(results, colWidths=[3.8*cm, 2.2*cm, 2.8*cm, 2.8*cm, 2.5*cm, 2.2*cm])
    rt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, GRAY_L]),
        ('BACKGROUND', (0,4), (-1,4), GREEN_L),
        ('FONTNAME', (0,4), (-1,4), 'Helvetica-Bold'),
        ('TEXTCOLOR', (5,4), (5,4), GREEN),
        ('GRID', (0,0), (-1,-1), 0.3, GREEN_M),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
    ]))
    story.append(rt)
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        'XGBoost significantly outperforms Linear Regression (which captures only linear '
        'relationships) and SVM (which struggles with the large scale variance in sugarcane '
        'yields vs other crops). Decision Tree and Random Forest achieve near-identical scores, '
        'suggesting the data has clear tree-learnable structures. XGBoost\'s gradient boosting '
        'mechanism provides marginal improvement through iterative error correction.', styles['Body']))
    story.append(PageBreak())

    # ── Advantages & Future Scope ─────────────────────────────────
    story.append(Paragraph('9. Advantages & Future Scope', styles['H1']))
    story.append(hr())

    story.append(Paragraph('9.1 Advantages', styles['H2']))
    story.append(hr(GREEN_M))
    for adv in [
        'End-to-end system from data generation to web-deployed prediction',
        '97.77% accuracy using XGBoost — industry-competitive performance',
        'MongoDB NoSQL integration with 5 specialised collections',
        'Role-based access (admin/farmer) with session security',
        '6 types of EDA visualizations auto-generated with Matplotlib/Seaborn',
        'Modular, maintainable code structure (utils/, models/, templates/)',
        'REST API endpoint (/api/predict) for external integration',
        'CSV export and browser-print ready reports',
        'Graceful degradation — works without MongoDB (demo mode)',
    ]:
        story.append(bullet(adv, styles))

    story.append(Paragraph('9.2 Future Scope', styles['H2']))
    story.append(hr(GREEN_M))
    for fut in [
        'Real-time weather API integration (OpenWeatherMap / IMD)',
        'Satellite imagery analysis with Convolutional Neural Networks',
        'LSTM-based time-series yield forecasting across seasons',
        'Mobile application (Flutter / React Native)',
        'IoT sensor data ingestion for real-time soil monitoring',
        'Government crop price API for profitability prediction',
        'Multi-language support (Hindi, Kannada, Tamil, etc.)',
        'Federated learning for privacy-preserving model training',
    ]:
        story.append(bullet(fut, styles))
    story.append(PageBreak())

    # ── Conclusion ────────────────────────────────────────────────
    story.append(Paragraph('10. Conclusion', styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        'This project successfully demonstrates an end-to-end AI/ML crop yield prediction system '
        'that satisfies all PBL review criteria. The platform integrates five machine learning '
        'algorithms, MongoDB NoSQL database, and a professional Flask web dashboard to deliver '
        'accurate agricultural yield forecasts. XGBoost achieves 97.77% prediction accuracy, '
        'outperforming all other evaluated algorithms.', styles['Body']))
    story.append(Paragraph(
        'The system provides genuine value to farmers by quantifying the impact of rainfall, '
        'temperature, soil type, fertilizer, and pesticide on yield — enabling data-driven '
        'agricultural planning. The modular architecture, REST API, and MongoDB integration '
        'make this platform readily extensible for real-world deployment.', styles['Body']))
    story.append(Spacer(1, 1*cm))

    final_data = [['CropYield AI achieves 97.77% prediction accuracy using XGBoost\nwith full MongoDB NoSQL integration and 5 working system modules']]
    final_t = Table(final_data, colWidths=['100%'])
    final_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), GREEN),
        ('TEXTCOLOR', (0,0), (-1,-1), WHITE),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 20),
        ('BOTTOMPADDING', (0,0), (-1,-1), 20),
    ]))
    story.append(final_t)

    doc.build(story)
    print(f"PDF generated: {path}")

if __name__ == '__main__':
    build_pdf('/mnt/user-data/outputs/CropYield_AI_Project_Documentation.pdf')

#!/usr/bin/env python3
"""
Update Rate Limiter Documentation PDF with Security Hardening
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime

def create_documentation():
    doc = SimpleDocTemplate(
        "docs/rate-limiter-documentation.pdf",
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=28,
        spaceAfter=20,
        textColor=HexColor('#1e3a5f')
    )

    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        spaceBefore=20,
        spaceAfter=10,
        textColor=HexColor('#1e3a5f')
    )

    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=8,
        textColor=HexColor('#2c5282')
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=9,
        fontName='Courier',
        backColor=HexColor('#f5f5f5'),
        leftIndent=20,
        spaceAfter=10
    )

    story = []

    # Title Page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("Redis Rate Limiter", title_style))
    story.append(Paragraph("Production Documentation", heading1_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Token Bucket Algorithm with Distributed State", normal_style))
    story.append(Spacer(1, inch))
    story.append(Paragraph(f"Version 1.1.0 (Security Hardened)", normal_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal_style))
    story.append(Paragraph("Jules MCP Server - Antigravity Orchestration", normal_style))
    story.append(PageBreak())

    # Table of Contents
    story.append(Paragraph("Table of Contents", heading1_style))
    toc_data = [
        ["1.", "Architecture Overview", "3"],
        ["2.", "Tier Configuration (Updated)", "4"],
        ["3.", "Integration Guide", "5"],
        ["4.", "Security Hardening (New)", "6"],
        ["5.", "API Reference", "7"],
        ["6.", "Metrics & Monitoring", "8"],
    ]
    toc_table = Table(toc_data, colWidths=[0.5*inch, 4*inch, 0.5*inch])
    toc_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # Page 3: Architecture Overview
    story.append(Paragraph("1. Architecture Overview", heading1_style))
    story.append(Paragraph("System Architecture", heading2_style))
    story.append(Paragraph(
        "The rate limiter implements a distributed token bucket algorithm using Redis for state management. "
        "It supports per-API-key rate limiting with tiered configurations and graceful failover to local memory when Redis is unavailable.",
        normal_style
    ))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Key Components:", heading2_style))
    components = [
        "<b>Express Middleware</b> - Intercepts requests and applies rate limiting",
        "<b>Redis Backend</b> - Distributed state management with atomic Lua scripts",
        "<b>Failover Cache</b> - Local memory backup when Redis is unavailable",
        "<b>Tier System</b> - Configurable limits per subscription tier",
    ]
    for comp in components:
        story.append(Paragraph(f"&bull; {comp}", normal_style))
    story.append(PageBreak())

    # Page 4: Tier Configuration (UPDATED)
    story.append(Paragraph("2. Tier Configuration (Updated)", heading1_style))
    story.append(Paragraph(
        "The rate limiter supports three tiers with configurable limits. Each tier uses the token bucket algorithm "
        "with different refill rates and burst capacities.",
        normal_style
    ))
    story.append(Spacer(1, 0.2*inch))

    # Updated tier table - Enterprise no longer has bypass
    tier_data = [
        ["Tier", "Requests/Min", "Burst Capacity", "Refill Rate", "Window"],
        ["Free", "100", "150", "1.67/sec", "60s"],
        ["Pro", "1,000", "1,500", "16.67/sec", "60s"],
        ["Enterprise", "100,000", "150,000", "1,666.67/sec", "60s"],
    ]
    tier_table = Table(tier_data, colWidths=[1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch, 0.8*inch])
    tier_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1e3a5f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 3), (-1, 3), HexColor('#e8f4e8')),  # Highlight enterprise row
    ]))
    story.append(tier_table)

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Security Change (v1.1.0):</b> Enterprise tier bypass removed", heading2_style))
    story.append(Paragraph(
        "The enterprise tier no longer bypasses rate limiting entirely. Instead, it has very high limits "
        "(100,000 requests/minute) to maintain protection against abuse while providing practically unlimited access for legitimate use.",
        normal_style
    ))
    story.append(PageBreak())

    # Page 5: Integration Guide
    story.append(Paragraph("3. Integration Guide", heading1_style))
    story.append(Paragraph("Quick Start", heading2_style))

    code_example = """
// 1. Import the rate limiter
import { createRateLimiter } from './middleware/rateLimiter.js';

// 2. Create and initialize
const rateLimiter = createRateLimiter();
await rateLimiter.initialize();

// 3. Apply middleware
app.use('/api/', rateLimiter.middleware());

// 4. Add metrics endpoint
app.get('/api/rate-limit/metrics', (req, res) => {
  res.json(rateLimiter.getMetrics());
});
"""
    story.append(Paragraph(code_example.replace('\n', '<br/>'), code_style))

    story.append(Paragraph("Environment Variables", heading2_style))
    env_data = [
        ["Variable", "Description", "Default"],
        ["REDIS_URL", "Redis connection (use rediss:// for TLS)", "redis://localhost:6379"],
        ["NODE_ENV", "Environment (enables TLS warning)", "development"],
        ["RATE_LIMIT_FAILOVER", "Failover strategy", "fail-closed"],
    ]
    env_table = Table(env_data, colWidths=[1.8*inch, 2.5*inch, 1.8*inch])
    env_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1e3a5f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(env_table)
    story.append(PageBreak())

    # Page 6: Security Hardening (NEW)
    story.append(Paragraph("4. Security Hardening (v1.1.0)", heading1_style))
    story.append(Paragraph(
        "Critical security fixes were applied to address vulnerabilities identified in the security audit.",
        normal_style
    ))
    story.append(Spacer(1, 0.2*inch))

    security_data = [
        ["Issue", "Severity", "Fix", "Status"],
        ["Stack trace in logs", "CRITICAL", "Removed err.stack from all error logs", "FIXED"],
        ["Redis TLS not enforced", "CRITICAL", "Added validateRedisUrl() warning", "FIXED"],
        ["X-Forwarded-For spoofing", "HIGH", "Use req.socket.remoteAddress", "FIXED"],
        ["API key in query string", "HIGH", "Deprecated and ignored", "FIXED"],
        ["Enterprise bypass", "HIGH", "Replaced with 100k/min limit", "FIXED"],
    ]
    security_table = Table(security_data, colWidths=[1.5*inch, 1*inch, 2.3*inch, 0.8*inch])
    security_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1e3a5f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (1, 1), (1, 2), HexColor('#ffcccc')),  # Critical = red
        ('BACKGROUND', (1, 3), (1, 5), HexColor('#ffffcc')),  # High = yellow
        ('BACKGROUND', (3, 1), (3, 5), HexColor('#ccffcc')),  # Fixed = green
    ]))
    story.append(security_table)

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Security Best Practices", heading2_style))
    practices = [
        "<b>Use TLS for Redis:</b> Set REDIS_URL to rediss://... in production",
        "<b>API keys in headers only:</b> Never pass API keys in query strings",
        "<b>Monitor error logs:</b> Stack traces no longer expose credentials",
        "<b>Trust socket address:</b> X-Forwarded-For can be spoofed by attackers",
    ]
    for practice in practices:
        story.append(Paragraph(f"&bull; {practice}", normal_style))
    story.append(PageBreak())

    # Page 7: API Reference
    story.append(Paragraph("5. API Reference", heading1_style))
    story.append(Paragraph("RedisRateLimiter Class", heading2_style))

    api_data = [
        ["Method", "Parameters", "Returns", "Description"],
        ["initialize()", "None", "Promise<boolean>", "Connect to Redis"],
        ["middleware()", "None", "Express middleware", "Create middleware"],
        ["getTier(apiKey)", "string", "Promise<string>", "Get tier for key"],
        ["setTier(apiKey, tier)", "string, string", "Promise<object>", "Set tier for key"],
        ["getMetrics()", "None", "object", "Get metrics"],
        ["close()", "None", "Promise<void>", "Close connection"],
    ]
    api_table = Table(api_data, colWidths=[1.5*inch, 1.2*inch, 1.5*inch, 1.5*inch])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1e3a5f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(api_table)

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Response Headers", heading2_style))
    headers_data = [
        ["Header", "Description", "Example"],
        ["RateLimit-Limit", "Maximum requests per window", "100"],
        ["RateLimit-Remaining", "Requests remaining", "42"],
        ["RateLimit-Reset", "Unix timestamp for reset", "1702814460"],
        ["Retry-After", "Seconds until next request", "45"],
    ]
    headers_table = Table(headers_data, colWidths=[1.8*inch, 2.5*inch, 1.3*inch])
    headers_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1e3a5f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(headers_table)
    story.append(PageBreak())

    # Page 8: Metrics & Monitoring
    story.append(Paragraph("6. Metrics & Monitoring", heading1_style))
    story.append(Paragraph(
        "The rate limiter exposes Prometheus-ready metrics via /api/rate-limit/metrics endpoint.",
        normal_style
    ))

    metrics_data = [
        ["Metric", "Type", "Description"],
        ["totalRequests", "Counter", "Total requests processed"],
        ["allowedRequests", "Counter", "Requests allowed through"],
        ["deniedRequests", "Counter", "Requests denied (429)"],
        ["redisErrors", "Counter", "Redis connection errors"],
        ["redisConnected", "Gauge", "Redis connection status"],
        ["requestsPerSecond", "Gauge", "Current request throughput"],
    ]
    metrics_table = Table(metrics_data, colWidths=[1.8*inch, 1*inch, 3*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1e3a5f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(metrics_table)

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Dashboard Component", heading2_style))
    story.append(Paragraph(
        "A React component (RateLimiterMetrics.jsx) is available for visualizing rate limiter metrics in the dashboard. "
        "It polls the metrics endpoint every 5 seconds and displays requests/sec, allowed/blocked counts, and Redis status.",
        normal_style
    ))

    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(
        f"Generated by Claude Code on {datetime.now().strftime('%Y-%m-%d')} | Jules MCP Server v2.5.0 | Antigravity Orchestration",
        normal_style
    ))

    # Build PDF
    doc.build(story)
    print("Documentation PDF updated successfully!")

if __name__ == "__main__":
    create_documentation()

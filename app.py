#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blog SEO Optimizer - Flask API Backend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path to import seo_optimizer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from seo_optimizer import SEOOptimizer

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize SEO Optimizer
optimizer = SEOOptimizer()

@app.route('/')
def home():
    """API home endpoint"""
    return jsonify({
        "message": "Blog SEO Optimizer API",
        "version": "1.0.0",
        "status": "running"
    })

@app.route('/api/optimize', methods=['POST'])
def optimize_content():
    """Optimize content endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['html_code', 'focus_keyword', 'seo_score']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"Missing required field: {field}"
                }), 400
        
        # Prepare input data
        input_data = {
            "html_code": data['html_code'],
            "focus_keyword": data['focus_keyword'],
            "seo_score": data['seo_score'],
            "categories": data.get('categories', ['Blog']),
            "tags": data.get('tags', []),
            "image": data.get('image', ''),
            "schema": data.get('schema', 'Article')
        }
        
        # Run optimization
        result = optimizer.optimize_content(input_data)
        
        # Return optimized result
        return jsonify({
            "success": True,
            "data": result
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Blog SEO Optimizer API"
    })

@app.route('/api/features', methods=['GET'])
def get_features():
    """Get available features"""
    return jsonify({
        "features": [
            {
                "name": "Title Tag Optimization",
                "description": "Optimize title tags with focus keywords (55-60 characters)",
                "icon": "⚡"
            },
            {
                "name": "Meta Description",
                "description": "Generate SEO-friendly meta descriptions (140-160 characters)",
                "icon": "📝"
            },
            {
                "name": "Keyword Density",
                "description": "Optimize keyword density to 1.5-2.5%",
                "icon": "🎯"
            },
            {
                "name": "Image Alt Text",
                "description": "Add SEO-friendly alt text to images",
                "icon": "🖼️"
            },
            {
                "name": "Link Optimization",
                "description": "Add internal and external links",
                "icon": "🔗"
            },
            {
                "name": "Schema Markup",
                "description": "Add structured data markup",
                "icon": "📊"
            }
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

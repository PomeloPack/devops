#!/bin/sh
echo "window.BACKEND_URL = '${BACKEND_URL:-http://localhost:5500}';" > /usr/share/nginx/html/env.js
nginx -g "daemon off;"
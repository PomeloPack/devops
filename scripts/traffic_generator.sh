#!/bin/bash

echo "🚀 Spouštím generátor provozu pro Grafanu..."
echo "zabij stisknutím CTRL+C"
echo "-------------------------------------------"

while true; do
  # Zavoláme hlavní stránku
  curl -s http://localhost:5500/ > /dev/null
  echo "GET / (Home) - OK"
  
  
  sleep 1
  
  # Zavoláme seznam měst
  curl -s http://localhost:5500/cities > /dev/null
  echo "GET /cities - OK"
  
  # Zavoláme health check
  curl -s http://localhost:5500/health > /dev/null
  echo "GET /health - OK"

  # Náhodná pauza 1 až 3 vteřiny, aby to vypadalo jako reálný člověk
  sleep $((1 + $RANDOM % 3))
done
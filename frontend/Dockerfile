FROM nginx:alpine

# Smažeme výchozí Nginx stránku
RUN rm -rf /usr/share/nginx/html/*

# Zkopírujeme tvůj index.html (a případně CSS/JS) do Nginxu
COPY index.html /usr/share/nginx/html/

# Zkopírujeme naši novou konfiguraci s přesměrováním na Backend
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
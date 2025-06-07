FROM nginx:1.25

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/html /usr/share/nginx/html
COPY ./project/audio/ /tmp/audio  

CMD mkdir -p /volume/mediafiles/audio && cp -r /tmp/audio/* /volume/mediafiles/audio/ && nginx -g "daemon off;"

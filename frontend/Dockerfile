FROM nginx:alpine
COPY nginx-vhost.conf /etc/nginx/conf.d/default.conf
RUN apk update
RUN apk add nodejs
ADD . /var/www
WORKDIR /var/www
RUN chown -R nginx /var/www
RUN npm install
RUN npm run build
EXPOSE 8080
CMD nginx -g 'daemon off;'

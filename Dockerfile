FROM python:3.7
LABEL Maintainer = "Mofesola Babalola <me@mofesola.com>"

WORKDIR /usr/src/app
COPY app .

EXPOSE 53/tcp 53/udp
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
CMD ["start_dns"]

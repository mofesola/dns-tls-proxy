FROM python:2.7.10
LABEL Maintainer = "Mofesola Babalola <me@mofesola.com>"

WORKDIR /usr/src/app
COPY app .

EXPOSE 53/tcp 53/udp
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
CMD ["start_dns"]
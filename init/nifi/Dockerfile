FROM apache/nifi:2.0.0-M1

ADD ./conf/ /opt/nifi/nifi-current/conf/

RUN ./bin/nifi.sh set-single-user-credentials admin admin_password
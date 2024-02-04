up:
ifdef service
	docker-compose up -d $(service);
else
	bash ./scripts/check_python.sh --up
	sudo docker compose up -d
	sudo docker compose exec nifi ./bin/nifi.sh set-single-user-credentials admin admin_password
endif

down:
ifdef service
	sudo docker compose down $(service);
else
	sudo docker compose down
	bash ./scripts/check_python.sh --down
endif

stop:
ifdef service
	sudo docker compose stop $(service);
else
	sudo docker compose stop
endif

start:
ifdef service
	sudo docker compose start $(service);
else
	sudo docker compose start
endif
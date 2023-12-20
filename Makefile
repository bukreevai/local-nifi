up:
ifdef service
	docker-compose up -d $(service);
else
	python -m scripts --up
	docker-compose up -d
endif

down:
ifdef service
	docker-compose down $(service);
else
	docker-compose down
	echo "Services stopped."
	python -m scripts --down
endif

stop:
ifdef service
	docker-compose stop $(service);
else
	docker-compose stop
endif

start:
ifdef service
	docker-compose start $(service);
else
	docker-compose start
endif
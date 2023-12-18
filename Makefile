up:
	gzip ./init/db/demo-medium-en-20170815.sql
	./scripts_nix/add_to_hosts.sh
ifdef service
	docker-compose up -d $(service);
else
	docker-compose up -d;
endif

down:
ifdef service
	docker-compose down $(service);
else
	docker-compose down;
	echo "Services stopped."
	./scripts_nix/remove_from_hosts.sh;
	echo "/etc/hosts is clear."
	rm -r ./nifi/*;
	rm -r ./postgres/*
	rm ./init/db/demo-medium-en-20170815.sql
endif

stop:
ifdef service
	docker-compose stop $(service);
else
	docker-compose stop;
endif

start:
ifdef service
	docker-compose start $(service);
else
	docker-compose start;
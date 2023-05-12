do:
	export PYTHONDONTWRITEBYTECODE=1
	docker-compose up -d --build --scale app=3
do:
	export PYTHONDONTWRITEBYTECODE=1
	docker-compose up -d --build --scale app=1 --scale db=1 --scale bucket=1 --remove-orphans
	
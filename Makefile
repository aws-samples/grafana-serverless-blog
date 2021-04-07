include etc/environment.sh

sam: sam.validate sam.build sam.deploy
sam.build: sam.validate
	sam build --use-container --parallel
sam.deploy:
	sam deploy
sam.validate:
	sam validate

invoke:
	aws lambda invoke --function-name ${FUNCTION} --invocation-type Event /dev/null &>/dev/null
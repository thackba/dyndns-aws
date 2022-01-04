.PHONY: clean prepare-test test package deploy

LAMBDA_DIR=./lambda
PACKAGE_DIR=./package

clean:
	if [ -d "${PACKAGE_DIR}" ]; then rm -r ${PACKAGE_DIR}; fi

prepare-test:
	if [ -f "./requirements-dev.txt" ]; then pip3 install -r ./requirements-dev.txt; fi

test:
	python3 -m unittest discover -v -s ${LAMBDA_DIR}

package: test clean
	mkdir -p ${PACKAGE_DIR}
	if [ -f "./requirements.txt" ]; then docker run -it --rm --name build-lambda -v $(PWD):/usr/src -w /usr/src python:3.9 pip install -r requirements.txt --target /usr/src/${PACKAGE_DIR}; fi
	rsync -r --exclude tests ${LAMBDA_DIR}/* ${PACKAGE_DIR}

deploy: package
	cd cdk && \
	npm run test && \
	cdk deploy DynDnsAwsDnsZoneStack && \
	cdk deploy DynDnsAwsLambdaFunctionStack && \
	cdk deploy DynDnsAwsApiGatewayStack
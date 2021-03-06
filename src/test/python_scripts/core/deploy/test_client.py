# Copyright 2011-2012 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import vertx
from test_utils import TestUtils
from core.event_bus import EventBus

tu = TestUtils()

print "in test"

class DeployTest(object):

    def test_deploy(self):

        def handler(message):
            if message.body == "started":
                tu.test_complete()
        EventBus.register_handler("test-handler", False, handler)
        conf = {'foo' : 'bar'}
        def deploy_handler(err, ok):
            tu.azzert(err == None)

        vertx.deploy_verticle("core/deploy/child.py", conf, 1, deploy_handler)

    def test_undeploy(self):
        print "in test undeploy"
        def handler(message):
            return

        EventBus.register_handler("test-handler", False, handler)

        conf = {'foo' : 'bar'}

        def undeploy_handler(err):
            tu.azzert(err == None)
            tu.test_complete()

        def deploy_handler(err, id):
            tu.azzert(err == None)
            vertx.undeploy_verticle(id, handler=undeploy_handler)

        vertx.deploy_verticle("core/deploy/child.py", conf, handler=deploy_handler)

    def test_deploy2(self):

        def deploy_handler(err, id):

            tu.azzert(err is None)
            tu.azzert(id is not None)

            def undeploy_handler(err):
                tu.azzert(err is None)
                tu.test_complete()

            vertx.undeploy_verticle(id, handler=undeploy_handler)

        vertx.deploy_verticle("core/deploy/child2.py", handler=deploy_handler)

    def test_deploy_fail(self):

        def deploy_handler(err, id):
            tu.azzert(err is not None)
            tu.azzert(id is None)
            tu.test_complete()

        vertx.deploy_verticle("core/deploy/notexists.py", handler=deploy_handler)

    def test_undeploy_fail(self):

        def undeploy_handler(err):
            tu.azzert(err is not None)
            tu.test_complete()

        vertx.undeploy_verticle("qijdqwijd", handler=undeploy_handler)

def vertx_stop():
    tu.unregister_all()
    tu.app_stopped()

tu.register_all(DeployTest())
tu.app_ready()

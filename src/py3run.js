var spawn = require("child_process").spawn;
var fs = require("fs");

module.exports = function(RED) {
    function Py3RunNode(config) {
        RED.nodes.createNode(this,config);
        var node = this;
        node.on('input', function(msg) {
            let fpath, args;
            if (msg.payload.hasOwnProperty("path")) {
                fpath = msg.payload.path;
            } else {
                fpath = config.path;
            }
            try {
                if (fs.existsSync(fpath)) {}
            } catch(err) {
                node.send(err);
                return;
            }
            if (msg.payload.hasOwnProperty("args")) {
                args = msg.payload.path;
            } else {
                args = config.args;
            }
            cmd = new Promise((resolve, reject) => {
                let p = spawn("python3", ["/data/python/runner.py", fpath, args]);
                let stdout, stderr, rc;
                p.stdout.on("data", (data) => { stdout = data });
                p.stderr.on("data", (data) => { stderr = data });
                p.on("exit", (code) => {
                    rc = code;
                    resolve({stdout, stderr, rc})
                });
            });

            cmd.then((data) => {
                node.send(data);
            });
        });
    }
    RED.nodes.registerType("py3run", Py3RunNode);
}

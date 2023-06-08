import searchGroup
import updateGroup

from flask import Flask, render_template, request
join = Flask(__name__)


@join.route("/")
def joinGroupUI():
    url = "joinGroup/joinGroup.html"
    return render_template(url)


@join.route("/joinGroup/in", methods=["POST"])
def joinGroupAuth():
    group_name = request.form.get("group_name")
    group_pass = request.form.get("group_pass")
    #result =
    searchGroup.searchGroup(group_name, group_pass)
    #if result = 0:
        #グループは存在しません
    #else:
        #グループに加入しました
        #
    updateGroup.updateGroup(123,"user")

if __name__ == "__main__":
    join.run()

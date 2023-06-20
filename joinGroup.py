import searchGroup
import updateGroup

from flask import Flask, render_template, request, redirect, url_for
join = Flask(__name__) # app


@join.route("/", methods=["GET", "POST"])  # @join.route("/joinGroup")
def joinGroupUI():
    if request.method == "GET":
        group_name = ""
        group_pass = ""
        url = "joinGroup/joinGroup.html"

    if request.method == "POST":
        group_name = str(request.form.get("group_name"))
        group_pass = str(request.form.get("group_pass"))
        if group_name == "" or group_pass == "":
            url = "joinGroup/joinGroup.html"
        else:
            userInput = request.form.get("userInput")
            if userInput == "True":
                return redirect(url_for("joinGroupAuth", group_name=group_name, group_pass=group_pass))
            elif userInput == "False":
                url = "joinGroup/joinGroup.html"

    return render_template(url, group_name=group_name, group_pass=group_pass, notExist="")


@join.route("/joinGroup/auth/<string:group_name>/<string:group_pass>")
def joinGroupAuth(group_name, group_pass):
    group_id = searchGroup.searchGroup(group_name, group_pass)
    if group_id == 0:
        url = "joinGroup/joinGroup.html"
        script = "<script>alert('入力されたグループは見つかりませんでした');</script>"
        return render_template(url, group_name=group_name, group_pass=group_pass, notExist=script)
    else:
        user_id = 3 # 仮
        updateGroup.updateGroup(user_id, group_id)
        url = "groupSchedule" # グループ画面のurl
        return "ok"  # return render_template(url)


if __name__ == "__main__":
    join.run()

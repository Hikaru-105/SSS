import searchGroup
import updateGroup

from flask import Flask, render_template, request, redirect, url_for
join = Flask(__name__)


@join.route("/", methods=["GET", "POST"])  # @join.route("/joinGroup")
def joinGroupUI():
    if request.method == "GET":
        url = "joinGroup/joinGroup.html"
        return render_template(url)

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
        return render_template(url)


@join.route("/joinGroup/auth/<string:group_name>/<string:group_pass>")
def joinGroupAuth(group_name, group_pass):
    print("auth") ###
    result = searchGroup.searchGroup(group_name, group_pass)
    if result == 0:
        # notExist
        print("notExist") ###
        url = "joinGroup/joinGroup.html"
    else:
        # success
        url = "groupSchedule"
        updateGroup.updateGroup(123, "user")
        print("success") ###
    return "ok"  # return render_template(url)


if __name__ == "__main__":
    join.run()


#グループ加入画面に戻る
#url = "joinGroup/joinGroup.html"
#return render_template(url)

#ダイアログ
# 確認........confirm
#存在しない...not_exist
#成功........success
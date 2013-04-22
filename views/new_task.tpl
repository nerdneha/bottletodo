%if error_msg:
{{error_msg}}   <br />
%end
<p> Add a new task to the ToDo list:</p>
 <form action="/add" method="POST">
   <input type="text" size="50" maxlength="50" name="task">
   <input type="submit" name="save" value="save">
 </form>

 <a href="/todo">See the full list</a>

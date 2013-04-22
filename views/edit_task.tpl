%#template for editing a task
%#the template expects to receive a value for "no" as well a "old", the text of the selected ToDo item

%if error_msg:
{{error_msg}} <br /> 
%end
<p>Edit the task with ID = {{num}}</p>
<form action="/edit" method="POST">
  <input type="text" name="task" value="{{old['task']}}" size="60" maxlength="100">
  <select name="status">
    <option>open</option>
    <option>closed</option>
  </select>
  <br/>
  <input type="submit" name="save" value="save">
  <input type="hidden" name="num" value="{{num}}">
</form>

<a href="/todo">See the full list</a>

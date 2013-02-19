%#template for editing a task
%#the template expects to receive a value for "no" as well a "old", the text of the selected ToDo item
<p>Edit the task with ID = {{no}}</p>
<form action="/edit" method="post">
  <input type="text" name="task" value="{{old['task']}}" size="100" maxlength="100">
  <select name="status">
    <option>open</option>
    <option>closed</option>
  </select>
  <br/>
  <input type="submit" name="save" value="save">
  <input type="hidden" name="no" value="{{no}}">
</form>

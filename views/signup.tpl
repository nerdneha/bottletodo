<a href="/login">HSers and Users, log in here!</a>
<p> Please sign in below: </p>
<form action="/signup" method="POST">
  <table>
    <tr>
      <td>Email: </td>
      <td> <input type="text" size="30" maxlength="50" name="email"> </td>
      <td>{{user_error}} </td>
      %if user_error:
        <td> <a href="/login">Login here!</a> </td>
      %end
    </tr>
    <tr>
        <td>Username: </td>
        <td> <input type="text" size="30" maxlength="50" name="username"> </td>
    <tr>
      <td>Password: </td>
      <td> <input type="password" size="30" maxlength="50" name="password">
      </td>
    </tr>
    <tr>
      <td>Confirm Password: </td>
      <td> <input type="password" size="30" maxlength="50" name="passwordconf">
      </td>
      %if pw_error:
      <td> {{pw_error}} </td>
      %end
    </tr>
    <tr>
      <td>What's your favorite food item?: </td>
      <td><input type="text" size="30" maxlength="50" name="food"> </td>
    </tr>
  </table>
  <input type="submit" name="submit" value="add me">
</form>

<a href="/login">If you already have an account, log in here!</a>

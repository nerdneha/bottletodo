<p> Please sign in below: </p>
<form action="/login" method="POST">
  <table>
    <tr>
      <td>Username: </td>
      <td> <input type="text" size="30" maxlength="50" name="username"> </td>
      <td>{{user_error}}
      <td> 
        % if user_error != "":
        <a href="/signup">Sign up for that username here!</a> </td>
        %end
    </tr>
    <tr>
      <td>Password: </td>
      <td> <input type="password" size="30" maxlength="50" name="password"> </td>
      <td> {{pw_error}} </td>
    </tr>
  </table>
  <input type="submit" name="submit" value="submit">
</form>

<a href="/signup">If you're new, create an account here!</a>

Welcome to the collaborative todo list - my first app that uses a db!
<p> Please sign in below with your Hackerschool Credentials or your login for this site: </p>
<form action="/login" method="POST">
  <table>
    <tr>
      <td>Email: </td>
      <td> <input type="text" size="30" maxlength="50" name="email"> </td>
      %if user_error:
      <td>{{user_error}}
      <td>
        <a href="/signup">Sign up for that email here!</a> </td>
        %end
    </tr>
    <tr>
      <td>Password: </td>
      <td> <input type="password" size="30" maxlength="50" name="password"> </td>
      %if pw_error:
      <td> {{pw_error}} </td>
      %end
    </tr>
  </table>
  <input type="submit" name="submit" value="submit">
</form>

<a href="/signup">If you're new, create an account here!</a> <br />
<a href="/anon">If you're just checking this out, view as anonymous here!</a>
<br>
<br>
<a href="https://github.com/nehalita/bottletodo">My GitHub Repo for this site</a>

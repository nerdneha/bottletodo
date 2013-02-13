%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p>The open tasks are:</p>

<ul>
  %for row in open_rows:
  <li>
    {{row[0]}}: {{row[1]}}
    <a href="/edit/{{row[0]}}">edit</a>
  </li>
  %end
</ul>

<p> The closed tasks are:</p>

<ul>
  %for row in closed_rows:
  <li>
    {{row[0]}}: {{row[1]}}
    <a href="/edit/{{row[0]}}">edit</a>
  </li>
  %end
</ul>

#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Bildiriler</h2>
  <table width="100%">
    <tr>
      <th width="25">No</th>
      <th>Başlık</th>
    </tr>
    #for $c,$i in enumerate($proposals)
      #if $c % 2
      <tr class="odd">
      #else
      <tr class="even">
      #end if
      <td><a href="viewproposal.py?pid=$i.pid&amp;version=$i.version">$i.pid</a></td>
      <td><a href="viewproposal.py?pid=$i.pid&amp;version=$i.version">$i.title</a></td>
    </tr>
    #end for
  </table>
  <p>&nbsp;</p>
  <p style="text-align: center;">
    #for $i in range(0, $pag_total)
      #if $i == $pag_now
        <b>#echo $i+1 #</b>
      #else
        <a href="proposals.py?start=$i">#echo $i+1 #</a>
      #end if
    #end for
  </p>
</div>
#include $site_path + "templates/footer.tpl"

<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/


if(GetRoleName($roleid) != "admin") {
	echo "Model silme işlemi için yetkiniz yok.";
	exit;
}
$ModelName = GetModelName($modelid);
$grpbrnd = GetGrpBrnd($modelid);
$grpid = GroupGrpBrnd($grpbrnd);
$brandid = BrandGrpBrnd($grpbrnd);
$groupname = GetGroupName($grpid);
$brandname = GetBrandName($brandid);
$newgrpbrnd = IsBrandGroup($newbrandid, $newgrpid);
$result_model_pv_statuses = mysql_query("select id from model_pv_status where model_id='$modelid'");
$j = 0;
while(($row_model_pv_statuses = mysql_fetch_row($result_model_pv_statuses)))
	$model_pv_statuses[$j++] = $row_model_pv_statuses[0];
$num_model_pv_statuses = $j;
$j = 0;
for($i=0; $i<$num_model_pv_statuses; $i++) {
	$result_comments = mysql_query("select id from comment where mpvs_id='$model_pv_statuses[$i]'");
	while(($row_comments = mysql_fetch_row($result_comments)))
		$comments[$j++] = $row_comments[0];
}
$num_comments = $j;
if($approved != true) {
	echo "<b>$groupname > $brandname > $ModelName</b> modeline ait bilgi:<br>\n";
	echo "<br><br> Durum bilgileri:<br>\n";
	for($i=0; $i<$num_model_pv_statuses; $i++)
		PrintModelPVStatus($model_pv_statuses[$i]);
	echo "<br><br> Bu durum bilgileriyle ilgli yorumlar:<br>\n";
	for($i=0; $i<$num_comments; $i++)
		PrintComment($comments[$i]);
	echo "
	 	<br>
     	<br>
	     <a href=\"?action=parameters&subaction=model_param&formsubmitted=true&grpid=$grpid&brandid=$brandid\">[GERİ]</a>&nbsp;&nbsp;&nbsp;<a href=\"?action=delmodel&modelid=$modelid&approved=true\">[SİL]</a>
	 	";
}
else {
	for($i=0; $i<$num_model_pv_statuses; $i++)
		mysql_query("delete from model_pv_status where id='$model_pv_statuses[$i]'");
	for($i=0; $i<$num_comments; $i++)
		mysql_query("delete from comment where id='$comments[$i]'");
	mysql_query("delete from model where id='$modelid'");
	mysql_query("optimize table model_pv_status");
	mysql_query("optimize table comment");
	mysql_query("optimize table pardus_version");
	$formsubmitted = true;
	$subaction = 'model_param';	
	require("model_param.php");
}
?>

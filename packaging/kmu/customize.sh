MODVER=`grep_prop version $MODPATH/module.prop`
MODVERCODE=`grep_prop versionCode $MODPATH/module.prop`

set_perm_recursive  $MODPATH  0  0  0755  0644

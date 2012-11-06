FILE=`ls -rt *.mar | tail -1`
VERSION="18.0a2"
SHA512=$(shasum -a 512 $FILE | sed 's/ .*//')
DATESTAMP=$(echo $FILE | sed 's/b2g_stable_update_//' | sed 's/\.mar//')
INI="application_${DATESTAMP}.ini"
BUILD_ID=$(grep BuildID= $INI | sed 's/BuildID=//')
SIZE=$(stat -c "%s" $FILE)
APPVERSION=$(grep ^Version= $INI | sed 's/Version=//')

cat update-template.xml \
  | sed "s/\\\$APPVERSION\\\$/$APPVERSION/g" \
  | sed "s/\\\$VERSION\\\$/$VERSION/g" \
  | sed "s/\\\$HASH\\\$/$SHA512/g" \
  | sed "s/\\\$SIZE\\\$/$SIZE/g" \
  | sed "s/\\\$BUILD_ID\\\$/$BUILD_ID/g" \
  | sed "s/\\\$FILE\\\$/$FILE/g" \
  > update.xml

cat update.xml


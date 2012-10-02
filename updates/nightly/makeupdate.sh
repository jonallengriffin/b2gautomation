#exit 0

FILE=`ls -rt *.mar | tail -1`
VERSION="18.0a1"
SHA512=$(shasum -a 512 $FILE | sed 's/ .*//')
BUILD_ID=$(echo $FILE | sed 's/b2g_update_//' | sed 's/\.mar//' | sed 's/[-_]//g')
SIZE=$(stat -c "%s" $FILE)

cat update-template.xml \
  | sed "s/\\\$VERSION\\\$/$VERSION/g" \
  | sed "s/\\\$HASH\\\$/$SHA512/g" \
  | sed "s/\\\$SIZE\\\$/$SIZE/g" \
  | sed "s/\\\$BUILD_ID\\\$/$BUILD_ID/g" \
  | sed "s/\\\$FILE\\\$/$FILE/g" \
  > update.xml

cat update.xml


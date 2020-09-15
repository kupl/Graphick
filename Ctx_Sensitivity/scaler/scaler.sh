CP="bin:lib/guava-23.0.jar"
MAIN="ptatoolkit.scaler.doop.Main"

#echo
#echo $*

java -Xmx48g -cp $CP $MAIN $*

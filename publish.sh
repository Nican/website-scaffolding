./build.sh
cd ..
rm -rf gpcz.github.com
git clone https://github.com/gpcz/gpcz.github.com.git
cd gpcz.github.com
cp -R ../website-scaffolding/deploy/* .
git add -A
if git commit; then
  git push
fi
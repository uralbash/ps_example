var autoprefixer = require('gulp-autoprefixer'),
    concat = require('gulp-concat'),
    gulp = require('gulp'),
    minifyCSS = require('gulp-minify-css'),
    notify = require("gulp-notify"),
    watch = require('gulp-watch');

var _ = require("underscore"),
    browserSync = require('browser-sync'),
    glob = require("glob"),
    minimatch = require("minimatch");

gulp.task('browser-sync', function() {
    browserSync({
        proxy: "localhost:8000",
    });
});

function getFiles (path) {
    var files = glob.sync(path + '**/*.css');
    target = minimatch.match(files, '__*.css', { matchBase: true });
    ignore = _.map(target, function(item){ return '!' + item; });
    result = files.concat(ignore);
    return result;
}

function getFileName (file) {
    return file.split('/').pop();
}

gulp.task('css', function() {

    var includes = glob.sync('./pyramid_sacrud_example/includes/*/');

    includes.forEach(function(folder){

        var includeName = folder.match(/.+\/(.+)\/$/)[1],
            includeFiles = getFiles('./pyramid_sacrud_example/includes/' + includeName + '/static/css/'),
            appFiles = [],
            appsNames = _.filter(glob.sync('../*/'), function(folder){
                var appFolder = folder.match(/.+\/(.+)\/$/)[1];
                return appFolder.indexOf(includeName) > -1;
            }),
            appName = _.first(appsNames);

        if (appName !== undefined) {
            appFiles = _.map(getFiles(appName + '*/static/css/'), function (item) {
                var appFileName = getFileName(item);
                includeFiles.forEach(function (include_item) {
                    var projectFileName = getFileName(include_item);
                    if (item.indexOf('!') === 0) { return item; }
                    if (appFileName === projectFileName) { item = '!' + item; }
                });
                return item;
            });
        }

        concatFiles = appFiles.concat(includeFiles);
        concatFiles = _.sortBy(concatFiles, function (item) { return item.indexOf('!') === 0; });
        concatFiles = _.uniq(concatFiles);

        gulp.src(concatFiles)
            .pipe(autoprefixer({
                browsers: [
                    'Firefox >= 3',
                    'Explorer >= 6',
                    'Opera >= 9',
                    'Chrome >= 15',
                    'Safari >= 4',
                    '> 1%'],
                cascade: false
            }))
            .pipe(minifyCSS())
            .pipe(concat('static/css/__' + includeName + '.css'))
            .pipe(gulp.dest(folder));
            //.pipe(notify("Generated file: <%= file.relative %>"));
    });
});



gulp.task('watch', function () {

    var path = './pyramid_sacrud_example/includes/*/static/';

    var files = glob.sync(path + '**/*.css'),
        target = minimatch.match(files, '__*.css', { matchBase: true }),
        ignore = _.map(target, function(item){ return '!' + item; });

    var watchFiles = files.concat(ignore);
        watchFiles.unshift(path + '**/*.css');

    watch(watchFiles, function (files, cb) {
        gulp.start('css', cb);
    });
});

gulp.task('default', ['watch']);
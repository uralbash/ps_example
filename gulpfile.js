var autoprefixer = require('gulp-autoprefixer'),
    concat = require('gulp-concat'),
    gulp = require('gulp'),
    gutil = require('gulp-util'),
    minifyCSS = require('gulp-minify-css'),
    watch = require('gulp-watch');

var _ = require("underscore"),
    browserSync = require('browser-sync'),
    fs = require('fs'),
    glob = require("glob"),
    minimatch = require("minimatch");

PROJECT_APPS_PATH = './pyramid_sacrud_example/includes/';
PROJECT_MODULES_PATH = '../*/';
PROJECT_STATIC_PATH = undefined;

function addWatchFolders(appName) {
    var modules = _.filter(glob.sync(PROJECT_MODULES_PATH), function(folder){
        moduleName = folder.match(/.+\/(.+)\/$/)[1];
        return moduleName.indexOf(appName) > -1;
    });
    var modulePath = _.first(modules);
    if (modulePath !== undefined) path = modulePath + appName + '/static/' + appName + '/css/**/*.css';
    else path = PROJECT_APPS_PATH + appName + '/static/' + appName + '/css/**/*.css' ;
    return path;
}

function getFiles(path) {
    if(path === undefined) { gutil.log(gutil.colors.red('Failed getFiles, files not found, "path" undefined')); }
    var files = glob.sync(path + '**/*.css'),
        target = minimatch.match(files, '__*.css', { matchBase: true }),
        ignore = _.map(target, function(item){ return '!' + item; }),
        result = files.concat(ignore);
    return result;
}

function getFileName(file) {
    return file.split('/').pop();
}

function getConcatFiles(appName) {
    var redefineModuleFiles = [],
        projectAppFiles = getFiles(PROJECT_APPS_PATH + appName + '/static/' + appName + '/css/');

    /* Find Redifine Modules */
    redefineModules = _.filter(glob.sync(PROJECT_MODULES_PATH), function(folder){
        redefineModuleName = folder.match(/.+\/(.+)\/$/)[1];
        return redefineModuleName.indexOf(appName) > -1;
    });

    redefineModulePath = _.first(redefineModules);

    if (redefineModulePath !== undefined) {
        /* Module Static Path Default Django */
        var path = redefineModulePath + appName + '/static/' + appName + '/css/';
        /* Redefine for Pyramid */
        if (fs.existsSync(path) === false) path = redefineModulePath + redefineModulePath.substring(3) + 'static/css/';
        redefineModuleFiles = _.map(getFiles(path), function (item) {
            var redefineFile = getFileName(item);
            projectAppFiles.forEach(function (include_item) {
                var projectFile = getFileName(include_item);
                if (item.indexOf('!') === 0) return item;
                if (redefineFile === projectFile) item = '!' + item;
            });
            return item;
        });
    }

    var concatFiles = redefineModuleFiles.concat(projectAppFiles);
    concatFiles = _.sortBy(concatFiles, function (item) { return item.indexOf('!') === 0; });
    concatFiles = _.uniq(concatFiles);
    return concatFiles;
}

function getExistConcatFile(appName) {
    var target = null,
        files = getFiles(PROJECT_APPS_PATH + appName + '/static/' + appName + '/css/');

    /* Find Not Redefined Modules */
    if (files.length <= 0) {
        modules = _.filter(glob.sync(PROJECT_MODULES_PATH), function(folder){
            moduleName = folder.match(/.+\/(.+)\/$/)[1];
            return moduleName.indexOf(appName) > -1;
        });
        modulePath = _.first(modules);
        if (modulePath !== undefined) target = modulePath + appName + '/static/' + appName + '/css/';
        else target = PROJECT_APPS_PATH + appName + '/static/' + appName + '/css/';
    } else {
        target = PROJECT_APPS_PATH + appName + '/static/' + appName + '/css/';
    }
    return target;
}

gulp.task('browser-sync', function() {
    browserSync({
        proxy: "localhost:8000",
    });
});

gulp.task('css', function() {
    var appList = glob.sync(PROJECT_APPS_PATH + '*/');
    appList.forEach(function(folder) {
        appName = folder.match(/.+\/(.+)\/$/)[1];
        gulp.src(getConcatFiles(appName))
            .pipe(autoprefixer({
                browsers: ['Firefox >= 3', 'Explorer >= 6', 'Opera >= 9', 'Chrome >= 15', 'Safari >= 4', '> 1%'],
                cascade: false
            }))
            .pipe(minifyCSS())
            .pipe(concat('__' + appName + '.css'))
            .pipe(gulp.dest(getExistConcatFile(appName)));
        gutil.log(gutil.colors.green('Create file: ' + getExistConcatFile(appName) + '__' + appName + '.css'));
    });

    if (PROJECT_STATIC_PATH !== undefined) {
        gulp.src(getFiles(PROJECT_STATIC_PATH))
            .pipe(autoprefixer({
                browsers: ['Firefox >= 3', 'Explorer >= 6', 'Opera >= 9', 'Chrome >= 15', 'Safari >= 4', '> 1%'],
                cascade: false
            }))
            .pipe(minifyCSS())
            .pipe(concat('__main.css'))
            .on('error', function (err) {
                gutil.log(gutil.colors.red('Failed to browserify'), gutil.colors.yellow(err.message));
            })
            .pipe(gulp.dest(PROJECT_STATIC_PATH));
        gutil.log(gutil.colors.green('Create file: ' + PROJECT_STATIC_PATH + '__main.css'));
    }
});

gulp.task('watch', function () {
    var app = glob.sync(PROJECT_APPS_PATH + '*/'),
        watchFiles = [];

    app.forEach(function(folder) {
        appName = folder.match(/.+\/(.+)\/$/)[1];
        watchFiles = watchFiles.concat(getConcatFiles(appName));
        watchFiles.push(addWatchFolders(appName));
    });

    watchFiles = watchFiles.concat(getFiles(PROJECT_STATIC_PATH));
    watchFiles.push(PROJECT_STATIC_PATH + '**/*.css');
    watchFiles = _.sortBy(watchFiles, function(item){ if (item.indexOf('!') !== 0) return item; });

    watch(watchFiles, function (files, cb) {
        gulp.start('css', cb);
        gutil.log(gutil.colors.yellow('Waiting...'));
    });
});

gulp.task('default', ['watch']);
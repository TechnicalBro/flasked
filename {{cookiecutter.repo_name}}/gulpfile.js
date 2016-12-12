var gulp = require('gulp'),
    bower = require('bower'),
    browserify = require('browserify'),
    size = require('gulp-size'),
    less = require('gulp-less'),
    coffee = require('gulp-coffee'),
    cjsx = require('gulp-cjsx'),
    cjsxify = require('cjsxify'),
    concat = require('gulp-concat'),
    source = require('vinyl-source-stream'),
    transform = require('vinyl-transform'),
    uglify = require('gulp-uglify'),
    minifyCss = require('gulp-minify-css'),
    stripJsComments = require('gulp-strip-comments'),
    stripCssComments = require('gulp-strip-css-comments'),
    sourcemaps = require('gulp-sourcemaps'),
    runSequence = require('run-sequence'),
    rename = require('gulp-rename'),
    replace = require('gulp-replace'),
    foreach = require('gulp-foreach'),
    clean = require('gulp-clean');

var static_dir = './{{cookiecutter.app_name}}/static';

var config = {
    jsxDir: static_dir + '/jsx/',
    libsDir: static_dir + "/libs/",
    jsDir: static_dir + '/js/',
    cssDir: static_dir + '/css/',
    lessDir: static_dir + '/less/',
    coffeeDir: static_dir + '/coffee/',
    publicDir: static_dir + '/public/'
};

gulp.task('build', function (callback) {
    runSequence('clean', 'build-interface', 'compress-js', 'concat-js', 'copy-scripts-js', 'build-styles', 'concat-css', 'copy-styles-css', 'copy-libs', 'clean-js-comments', 'clean-css-comments', callback);
    console.log("Build Operation Complete!");
});

gulp.task('build-interface', function (callback) {
    return browserify({
        insertGlobals: true,
        entries: [config.jsxDir + 'interface.cjsx'],
        transform: [cjsxify],
        debug: true,
        extensions: ['.cjsx']
    })
        .bundle()
        .pipe(source('ui.js'))
        .pipe(gulp.dest(config.publicDir + "js/"))
});

gulp.task('build-styles', function (callback) {
    return gulp.src(config.lessDir + "**/*.less")
        .pipe(less())
        .pipe(gulp.dest(config.cssDir))
        .pipe(size());
});

gulp.task('clean', function (callback) {
    return gulp.src([config.jsDir + '**/*.js', config.cssDir + '**/*.css', config.publicDir + '**/*.css', config.publicDir + '**/*.js'], {
        read: false
    })
        .pipe(clean());
});

gulp.task('concat-js', function () {
    return gulp.src(config.jsDir + "*.js")
        .pipe(sourcemaps.init())
        .pipe(concat("scripts.min.js"))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(config.jsDir))
        .pipe(size());

});

gulp.task('compress-js', function () {
    return gulp.src(config.jsDir + "**/*.js")
        .pipe(sourcemaps.init())
        .pipe(uglify())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(config.jsDir));
});

gulp.task('copy-scripts-js', function () {
    return gulp.src(config.jsDir + "scripts.min.js").pipe(gulp.dest(config.publicDir + "js/")).pipe(size());

});

gulp.task('clean-js-comments', function (callback) {
    gulp.src(config.publicDir + "js/**/*.js").pipe(stripJsComments()).pipe(gulp.dest(config.publicDir + "js/"));
    callback();
});


gulp.task('concat-css', function () {
    return gulp.src(config.cssDir + "**/*.css")
        .pipe(sourcemaps.init())
        .pipe(concat("styles.min.css"))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(config.cssDir))
        .pipe(size());
});


gulp.task('compress-css', function () {
    return gulp.src(config.cssDir + "**/*.css")
        .pipe(sourcemaps.init())
        .pipe(minifyCss())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(config.cssDir))
        .pipe(size());
});


gulp.task('copy-styles-css', function () {
    return gulp.src(config.cssDir + "styles.min.css").pipe(gulp.dest(config.publicDir + "css/"));

});

gulp.task('clean-css-comments', function () {
    return gulp.src(config.publicDir + "css/**/*.css").pipe(stripCssComments()).pipe(gulp.dest(config.publicDir + "css/"));
});

gulp.task('default', function () {
    runSequence('build');
});

gulp.task('copy-libs', function (callback) {
    gulp.src('./{{cookiecutter.app_name}}/static/libs/jQuery/dist/jquery.min.js').pipe(gulp.dest(config.publicDir + "js/"));

    gulp.src('./{{cookiecutter.app_name}}/static/libs/bootstrap/dist/js/bootstrap.min.js').pipe(gulp.dest(config.publicDir + "js/"));
    gulp.src('./{{cookiecutter.app_name}}/static/libs/bootstrap/dist/css/bootstrap.min.css').pipe(gulp.dest(config.publicDir + "css/"));
    gulp.src('./{{cookiecutter.app_name}}/static/libs/components-font-awesome/fonts/**/*.*').pipe(gulp.dest(config.publicDir + 'fonts/'));
    gulp.src('./{{cookiecutter.app_name}}/static/libs/bootstrap/dist/fonts/**/*.*').pipe(gulp.dest(config.publicDir + 'fonts/'));
    gulp.src('./{{cookiecutter.app_name}}/static/libs/components-font-awesome/css/font-awesome.min.css').pipe(gulp.dest(config.publicDir + 'css/'));

    gulp.src('./{{cookiecutter.app_name}}/static/libs/react/react-with-addons.min.js').pipe(gulp.dest(config.publicDir + 'js/'));
    gulp.src('./{{cookiecutter.app_name}}/static/libs/react/react-with-addons.js').pipe(gulp.dest(config.publicDir + 'js/'));
    gulp.src('./{{cookiecutter.app_name}}/static/libs/react/react-dom.min.js').pipe(gulp.dest(config.publicDir + 'js/'));
    gulp.src('./{{cookiecutter.app_name}}/static/libs/react/react-dom.js').pipe(gulp.dest(config.publicDir + 'js/'));

    gulp.src('./{{cookiecutter.app_name}}/static/libs/remarkable-bootstrap-notify/dist/bootstrap-notify.min.js').pipe(gulp.dest(config.publicDir + "js"));

    gulp.src('./{{cookiecutter.app_name}}/static/libs/react-bootstrap-table/react-bootstrap-table.min.js').pipe(gulp.dest(config.publicDir + "js/"));
    gulp.src('./{{cookiecutter.app_name}}/static/libs/react-bootstrap-table/react-bootstrap-table-all.min.css').pipe(gulp.dest(config.publicDir + "css/"));

    gulp.src('./{{cookiecutter.app_name}}/static/libs/animate.css/animate.min.css').pipe(gulp.dest(config.publicDir + "css/"));

    callback();
});

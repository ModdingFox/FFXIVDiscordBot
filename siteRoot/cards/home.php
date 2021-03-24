<div class="card-body d-none" id="homeCardBody">
    <div><h1 class="card-title">Club Spectrum</h1></div>
    <div><h2 class="card-text">Show us your true colors!</h2></div>
    <div id="carouselDiv" class="carousel slide" data-ride="carousel">
        <ol class="carousel-indicators">
            <?php
                $files = preg_grep('/^([^.])/', scandir($_SERVER['DOCUMENT_ROOT'] . "/img/home"));
                $filesCount = count($files);
                for ($x = 0; $x <= $filesCount; $x++) {
                    if ($x == 0) {
                        echo '<li data-target="#carouselDiv" data-slide-to="0" class="active"></li>';
                    } else {
                        echo '<li data-target="#carouselDiv" data-slide-to="' . $x . '"></li>';
                    }
                }
            ?>
        </ol>
        <div class="carousel-inner">
            <?php
                $files = preg_grep('/^([^.])/', scandir($_SERVER['DOCUMENT_ROOT'] . "/img/home"));
                $isFirst = True;
                foreach ($files as &$file) {
                    if ($isFirst == True) {
                        echo '<div class="carousel-item active">';
                        $isFirst = False;
                    } else {
                        echo '<div class="carousel-item">';
                    }
                    echo '<img class="d-block w-100" src="/img/home/' . $file . '" alt="">';
                    echo '</div>';
                }
            ?>
        </div>
        <a class="carousel-control-prev" href="#carouselDiv" role="button" data-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="sr-only">Previous</span>
        </a>
        <a class="carousel-control-next" href="#carouselDiv" role="button" data-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="sr-only">Next</span>
        </a>
    </div>
</div>

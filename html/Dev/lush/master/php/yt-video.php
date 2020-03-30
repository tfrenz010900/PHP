<?php

// Paste here your Youtube API KEY
// https://developers.google.com/youtube/v3/getting-started
define("YT_API_KEY", "");

// Expect a param in the form "?vid=VIDEO_ID"
$video_id = $_GET['vid'];

// If param exists, request video data to youtube
if(isset($video_id)) {
    $video_data = Youtube::getVideoInfo($video_id);
}
else {
    $video_data =  array(
        'error' => 'No video ID provided.'
    );
}

// Encode the resulting data
echo json_encode($video_data);


/// Note:
/// Minumun JSON structure require for the slider to work with youtube videos
/// {
///     "duraction_sec": "Video duration in seconds"
///     "thumbnail": {
///         "maxresDefault": "Full URL to the maxresDefault video preview"
///     }
/// }
/// * Any other options are not used by the slider.


///////

class Youtube
{
    // http://stackoverflow.com/a/30761150/1754325
    static $api_key = YT_API_KEY;
    static $api_base = 'https://www.googleapis.com/youtube/v3/videos';
    static $thumbnail_base = 'https://i.ytimg.com/vi/';

    // $vid - video id in youtube
    // returns - video info
    public static function getVideoInfo($vid)
    {
        $params = array(
            'part' => 'contentDetails',
            'id' => $vid,
            'key' => self::$api_key,
        );

        $api_url = Youtube::$api_base . '?' . http_build_query($params);
        $result = json_decode(@file_get_contents($api_url), true);

        if(empty($result['items'][0]['contentDetails']))
            return null;
        $vinfo = $result['items'][0]['contentDetails'];

        $interval = new DateInterval($vinfo['duration']);
        $vinfo['duration_sec'] = $interval->h * 3600 + $interval->i * 60 + $interval->s;

        $vinfo['thumbnail']['default']       = self::$thumbnail_base . $vid . '/default.jpg';
        $vinfo['thumbnail']['mqDefault']     = self::$thumbnail_base . $vid . '/mqdefault.jpg';
        $vinfo['thumbnail']['hqDefault']     = self::$thumbnail_base . $vid . '/hqdefault.jpg';

        $vinfo['thumbnail']['sdDefault']     = self::$thumbnail_base . $vid . '/sddefault.jpg';
        $vinfo['thumbnail']['maxresDefault'] = self::$thumbnail_base . $vid . '/maxresdefault.jpg';

        return $vinfo;
    }
}
?>
from enum import Enum

RELATIONSHIPS_PARAMS = {}
RELATIONSHIPS_PARAMS["extend"] = "editorialArtwork,editorialVideo,offers,seoDescription,seoTitle,trackCount"

RELATIONSHIPS_PARAMS["fields[albums]"] = "artistName,artistUrl,contentRating,genreNames,isCompilation,isComplete,isMasteredForItunes,isSingle,recordLabel,releaseDate,trackCount,name,artwork,playParams,url"
RELATIONSHIPS_PARAMS["fields[apple-curators]"] = "name,url"
RELATIONSHIPS_PARAMS["fields[artists]"] = "name,artwork,url,genreNames,editorialNotes"
RELATIONSHIPS_PARAMS["fields[curators]"] = "name,url"
RELATIONSHIPS_PARAMS["fields[songs]"] = "name,artistName,ComposerName,albumName,trackNumber,discNumber,genreNames,durationInMillis,releaseDate,url,artistName,curatorName,composerName,artwork,playParams,contentRating,albumName,url,durationInMillis,audioTraits,extendedAssetUrls"

RELATIONSHIPS_PARAMS["include"] = "tracks,curator"
RELATIONSHIPS_PARAMS["include[music-videos]"] = "artists"
RELATIONSHIPS_PARAMS["include[songs]"] = "artists,genres,albums,composers"
RELATIONSHIPS_PARAMS["include[stations]"] = "tracks"
RELATIONSHIPS_PARAMS["l"] = "en-US"

class AppleTypes(Enum):
    PLAYLIST = "playlists"
    TRACK = "songs"
    ALBUM = "albums"
    ARTIST = "artists"
    VIDEO = "videos"
    GENRE = "genres"

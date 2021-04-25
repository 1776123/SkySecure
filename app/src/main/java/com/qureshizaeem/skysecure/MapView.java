package com.qureshizaeem.skysecure;

import androidx.annotation.NonNull;

private MapView mapView;

@Override
protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Mapbox.getInstance(this, getString(R.string.mapbox_access_token));

        setContentView(R.layout.mapper);

        mapView = (MapView) findViewById(R.id.mapView);
        mapView.onCreate(savedInstanceState);
        mapView.getMapAsync(new OnMapReadyCallback() {
@Override
public void onMapReady(@NonNull MapboxMap mapboxMap) {

        mapboxMap.setStyle(Style.MAPBOX_STREETS, new Style.OnStyleLoaded() {
@Override
public void onStyleLoaded(@NonNull Style style) {
        mapboxMap?.addMarker(MarkerOptions()
        .position(LatLng(48.85819, 2.29458))
        .title("Eiffel Tower"));
        // Map is set up and the style has loaded. Now you can add data or make other map adjustments}
        });

        }
        });
        }
        @Override
protected void onStart() {
        super.onStart();
        mapView.onStart();
        }

@Override
protected void onResume() {
        super.onResume();
        mapView.onResume();
        }

@Override
protected void onPause() {
        super.onPause();
        mapView.onPause();
        }

@Override
protected void onStop() {
        super.onStop();
        mapView.onStop();
        }

@Override
protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        mapView.onSaveInstanceState(outState);
        }

@Override
public void onLowMemory() {
        super.onLowMemory();
        mapView.onLowMemory();
        }

@Override
protected void onDestroy() {
        super.onDestroy();
        mapView.onDestroy();
        }




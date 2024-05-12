import React, { useState, useEffect, useRef } from 'react';
import './Map.css';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { ENV } from '../../constants';

mapboxgl.accessToken = ENV.MAPBOX_API_TOKEN;

const colors = ['#392A48', '#A865B5', '#301934', '#B6B5D8', '#856088', '#524F81', '#4B0082', '#633974', '#512E5F', '#4A235A'];

const MapDisplay = () => {
  const [vehicles, setVehicles] = useState([]);
  const mapRef = useRef(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const baseURL = ENV.API_BASE_URL_9000;
        const response = await fetch(`${baseURL}/supply-services/fleet/get-vehicles-info`);
        const data = await response.json();
        const validVehicles = data.filter(vehicle =>
          Array.isArray(vehicle.current_location) &&
          vehicle.current_location.length === 2 &&
          vehicle.current_location.every(coord => typeof coord === 'number' && !isNaN(coord)) &&
          Math.abs(vehicle.current_location[1]) <= 90
        )
        .map(vehicle => ({
          ...vehicle,
          route: vehicle.route ? JSON.parse(vehicle.route).filter(coordPair =>
            Array.isArray(coordPair) &&
            coordPair.length === 2 &&
            coordPair.every(coord => typeof coord === 'number' && !isNaN(coord)) &&
            Math.abs(coordPair[1]) <= 90
          ) : null
        }));
        setVehicles(validVehicles);
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };
    fetchData();
  }, []);

  useEffect(() => {
    const map = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/streets-v11',
      center: [-97.7431, 30.2672],
      zoom: 11
    });
    mapRef.current = map;

    map.on('load', () => {
      vehicles.forEach((vehicle, index) => {
        if (vehicle.route && vehicle.route.length > 0) {
          const routeId = `route${vehicle.VehicleID}`;
          const color = colors[index % colors.length];
          const coordinates = vehicle.route;

          map.addSource(routeId, {
            type: 'geojson',
            data: {
              type: 'Feature',
              properties: {},
              geometry: {
                type: 'LineString',
                coordinates: coordinates
              }
            }
          });

          map.addLayer({
            id: routeId,
            type: 'line',
            source: routeId,
            layout: {
              'line-join': 'round',
              'line-cap': 'round'
            },
            paint: {
              'line-color': color,
              'line-width': 4
            }
          });

          const elCar = document.createElement('div');
          elCar.className = 'custom-car-icon';

          const carMarker = new mapboxgl.Marker(elCar, { anchor: 'center' })
            .setLngLat(coordinates[0])
            .addTo(map);

          carMarker.getElement().addEventListener('click', () => {
            new mapboxgl.Popup({ offset: 25 })
              .setLngLat(carMarker.getLngLat())
              .setText(`Vehicle ID: ${vehicle.VehicleID}`)
              .addTo(map);
          });

          function animateCar() {
            carMarker.setLngLat(vehicle.current_location); // lets car at its long and lat position
          }
          animateCar();

          if (coordinates.length > 1) {
            map.addLayer({
              id: `start-${routeId}`,
              type: 'circle',
              source: {
                type: 'geojson',
                data: {
                  type: 'Feature',
                  geometry: {
                    type: 'Point',
                    coordinates: coordinates[0]
                  }
                }
              },
              paint: {
                'circle-radius': 3,
                'circle-color': '#FF0000'
              }
            });

            map.addLayer({
              id: `end-${routeId}`,
              type: 'circle',
              source: {
                type: 'geojson',
                data: {
                  type: 'Feature',
                  geometry: {
                    type: 'Point',
                    coordinates: coordinates[coordinates.length - 1]
                  }
                }
              },
              paint: {
                'circle-radius': 3,
                'circle-color': '#008000'
              }
            });
          }
        }
      });
    });

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
      }
    };
  }, [vehicles]);

  return <div id="map" style={{ position: 'absolute', top: 0, bottom: 0, width: '100%' }}></div>;
};

export default MapDisplay;

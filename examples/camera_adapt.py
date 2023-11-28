import carla


def main():
    try:
        # Connect to the Carla server
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)  # Adjust timeout if necessary

        # Load the Town 04 map
        world = client.load_world('Town04')

        # Get a blueprint for the vehicle
        blueprint_library = world.get_blueprint_library()
        vehicle_bp = blueprint_library.find('vehicle.tesla.model3')

        # Set the spawn point for the ego vehicle
        spawn_point = carla.Transform(carla.Location(x=100, y=100, z=2), carla.Rotation())

        # Spawn the ego vehicle
        ego_vehicle = world.spawn_actor(vehicle_bp, spawn_point)

        # Add a camera sensor to the ego vehicle
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_transform = carla.Transform(carla.Location(z=50))
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=ego_vehicle)

        # Configure the camera sensor settings
        camera.set_attribute('image_size_x', '800')
        camera.set_attribute('image_size_y', '600')
        camera.set_attribute('fov', '90')

        # Function to process the image data captured by the camera
        def process_image(image):
            image.save_to_disk('output/image.png')  # Save the image to disk
            # Implement your image processing or analysis here

        # Register the callback function to process the image data
        camera.listen(process_image)

        input("Press Enter to exit...\n")  # Keep the script running

    except RuntimeError as e:
        print(f"An error occurred: {e}")

    finally:
        # Clean up actors if available
        if 'camera' in locals():
            camera.destroy()
        if 'ego_vehicle' in locals():
            ego_vehicle.destroy()


if __name__ == '__main__':
    main()

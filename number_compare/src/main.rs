
use std::collections::HashMap;

struct PathFinder {
    reference: Vec<i32>,
    input: Vec<i32>,
    node_paths: HashMap<(i32,i32), (Vec<(i32,i32)>, bool)>,
    best_path: Vec<(i32,i32)>,
}

fn get_path_value(path: &Vec<(i32,i32)>) -> i32 {
    let true_value_change: i32 = -3;
    return path[path.len() -1].0+path[path.len() -1].1 + (path.len()-1) as i32 *true_value_change;
}

fn initialize_PathFinder(pathfinder: &mut PathFinder, reference_number: Vec<i32>, input_number: Vec<i32>) {
    pathfinder.reference = reference_number;
    pathfinder.input = input_number;
    pathfinder.node_paths = initialize_node_paths(&pathfinder.reference, &pathfinder.input);
    pathfinder.node_paths = find_best_path_for_each_node();
    pathfinder.best_path = find_best_path(pathfinder.node_paths);
}

fn initialize_node_paths(reference: &Vec<i32>, input: &Vec<i32>) -> HashMap<(i32,i32), (Vec<(i32,i32)>, bool)> {
    let mut node_paths: HashMap<(i32,i32), (Vec<(i32,i32)>, bool)> = HashMap::new();
    node_paths.insert((0,0), (Vec::new(), true));
    for i in 0..reference.len() {
        for j in 0..input.len() {
            if reference[j] == input[i] {
                node_paths.insert((i as i32, j as i32), (vec![0,0], true));
            }
        }
    }
    return node_paths;
}



fn main() {
    println!("Hello, world!");
}
